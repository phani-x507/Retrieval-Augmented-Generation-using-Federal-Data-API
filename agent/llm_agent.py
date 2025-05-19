import openai
import json
import asyncio
from agent.tool_calls import fetch_from_db

# Setting the base URL for the local LLM (Ollama)
openai.api_base = "http://localhost:11434/v1"  # Adjust as per your Ollama setup
openai.api_key = "dummy_key"

async def run_tool(tool_name, arguments):
    if tool_name == "fetch_from_db":
        query = arguments.get("query", "")
        result = await fetch_from_db(query)
        return result
    return "Tool not found."

async def llm_agent(user_query):
    try:
        # Define the system prompt
        system_prompt = """
You are a data agent. If the user asks for information that requires database access, always respond ONLY with a JSON object in this format:
{"tool": "fetch_from_db", "arguments": {"query": "<SQL QUERY HERE>"}}
Do not answer in any other way. Here is an example:
User: Show recent executive orders
LLM: {"tool": "fetch_from_db", "arguments": {"query": "SELECT title, publication_date FROM federal_register ORDER BY publication_date DESC LIMIT 5"}}
"""
        
        # Updated call for local Ollama LLM
        response = openai.Completion.create(
            model="qwen:1.8b",  # Adjust the model name as needed
            prompt=f"{system_prompt}\nUser: {user_query}\n",
            max_tokens=100,
            temperature=0.7,
        )

        # Extract and parse the response
        llm_output = response['choices'][0]['text'].strip()
        print("LLM Output:", llm_output)
        try:    
            tool_call = json.loads(llm_output)
            print("Tool call detected:", tool_call)
            # Check if the response contains a tool call
            tool_name = tool_call.get("tool", "")
            arguments = tool_call.get("arguments", {})

            # Run the tool if specified
            if tool_name:
                result = await run_tool(tool_name, arguments)
                return str(result)
            else:
                return llm_output

        except json.JSONDecodeError:
            return llm_output

    except Exception as e:
        return f"Error: {str(e)}"
