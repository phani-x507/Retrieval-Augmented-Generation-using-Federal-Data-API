

from fastapi import FastAPI
import openai
import json
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pipeline_runner import run_pipeline  # Import the pipeline function
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await run_pipeline()  # This will run ONCE at startup
    yield

app = FastAPI(lifespan=lifespan)


# Add this after app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify ["http://localhost:3000"] for React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

# LLM Configuration
openai.api_base = "http://localhost:11434/v1"
openai.api_key = "dummy_key"

# Database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "fd_data"
}


@app.get("/run_pipeline")
async def trigger_pipeline():
    try:
        # Directly await the pipeline coroutine without using asyncio.run()
        pipeline_result = await run_pipeline()
        return {"message": pipeline_result}
    except Exception as e:
        return {"error": str(e)}

def execute_sql_query(query):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        # Formatting the result for better readability
        formatted_result = [f"Title: {row[0]}, Date: {row[1]}" for row in result]
        return formatted_result
    except Exception as e:
        return f"SQL Error: {str(e)}"

@app.post("/chat")
async def chat(request: QueryRequest):
    query = request.query
    system_prompt = """
You are a data agent. If the user asks for information that requires database access, always respond ONLY with a JSON object in this format:
{"tool": "fetch_from_db", "arguments": {"query": "<SQL QUERY HERE>"}}
If the user asks a general or casual question that does NOT require database access, answer normally in plain text.
Do not answer database questions in any way except the JSON tool call format.
Here is an example:
User: Show recent executive orders
LLM: {"tool": "fetch_from_db", "arguments": {"query": "SELECT title, publication_date FROM federal_register ORDER BY publication_date DESC LIMIT 5"}}
User: Who is the president of the United States?
LLM: The current president of the United States is Joe Biden.
"""
    try:
        response = openai.ChatCompletion.create(
            model="llama2:latest",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
        )
        llm_response = response['choices'][0]['message']['content']

        # Try to extract JSON object from the response
        import re
        match = re.search(r'\{.*\}', llm_response, re.DOTALL)
        if match:
            json_candidate = match.group(0)
            try:
                llm_output = json.loads(json_candidate)
                if "tool" in llm_output:
                    tool_name = llm_output["tool"]
                    arguments = llm_output.get("arguments", {})
                    normalized_tool = tool_name.replace(" ", "").replace("_", "").lower()
                    if normalized_tool == "fetchfromdb":
                        sql_query = arguments.get("query")
                        if sql_query and "federal_register" in sql_query.lower():
                            db_result = execute_sql_query(sql_query)
                            return {"response": db_result}
                        else:
                            return {"response": "Sorry, I can only answer questions about the 'federal_register' table."}
                    else:
                        return {"response": f"Unknown tool: {tool_name}"}
            except json.JSONDecodeError:
                pass  # Not a valid JSON, treat as plain text

        # If not a tool call, return the LLM's plain text answer
        return {"response": llm_response.strip()}

    except Exception as e:
        return {"response": f"LLM Error: {str(e)}"}
