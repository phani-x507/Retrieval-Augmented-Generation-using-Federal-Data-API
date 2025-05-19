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
    try:
        # Get response from LLM
        response = openai.ChatCompletion.create(
            model="qwen:0.5b",
            messages=[{"role": "user", "content": query}]
        )
        llm_response = response['choices'][0]['message']['content']

        # Try to parse the response to check for tool calls
        try:
            llm_output = json.loads(llm_response)
            if "tool" in llm_output:
                tool_name = llm_output["tool"]
                arguments = llm_output.get("arguments", {})

                # Handling the tool call
                if tool_name == "fetch_from_db":
                    sql_query = arguments.get("query")
                    if sql_query:
                        db_result = execute_sql_query(sql_query)
                        return {"response": db_result}
                    return {"response": "Error: No query provided."}
                else:
                    return {"response": f"Unknown tool: {tool_name}"}
            else:
                return {"response": llm_response}
        except json.JSONDecodeError:
            # Directly return if no tool call found
            return {"response": llm_response}

    except Exception as e:
        return {"response": f"LLM Error: {str(e)}"}
