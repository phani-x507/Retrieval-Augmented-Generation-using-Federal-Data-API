# import asyncio
# from data_pipeline.downloader import download_data
# from data_pipeline.processor import process_data
# from data_pipeline.db_updater import update_database

# async def run_pipeline():
#     print("Starting data pipeline...")
#     await download_data()
#     process_data()
#     await update_database()
#     print("Pipeline executed successfully.")

# asyncio.run(run_pipeline())


from fastapi import FastAPI
import openai
import json
import mysql.connector

app = FastAPI()

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
async def chat(query: str):
    system_prompt = """
You are a data agent. If the user asks for information that requires database access, always respond ONLY with a JSON object in this format:
{"tool": "fetch_from_db", "arguments": {"query": "<SQL QUERY HERE>"}}
Do not answer in any other way. Here is an example:
User: Show recent executive orders
LLM: {"tool": "fetch_from_db", "arguments": {"query": "SELECT title, publication_date FROM federal_register ORDER BY publication_date DESC LIMIT 5"}}
"""
    try:
        # Use system and user roles properly
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
            llm_response = match.group(0)

        # Try to parse the response to check for tool calls
        try:
            llm_output = json.loads(llm_response)
            if "tool" in llm_output:
                tool_name = llm_output["tool"]
                arguments = llm_output.get("arguments", {})

                # Handling the tool call
            normalized_tool = tool_name.replace(" ", "").replace("_", "").lower()
            if normalized_tool == "fetchfromdb":
                sql_query = arguments.get("query")
                if sql_query:
                    db_result = execute_sql_query(sql_query)
                    return {"response": db_result}
                return {"response": "Error: No query provided."}
            else:
                return {"response": f"Unknown tool: {tool_name}"}
            
        except json.JSONDecodeError:
            # Directly return if no tool call found
            return {"response": llm_response}

    except Exception as e:
        return {"response": f"LLM Error: {str(e)}"}
