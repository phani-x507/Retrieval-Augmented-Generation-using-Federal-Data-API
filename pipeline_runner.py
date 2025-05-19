import asyncio
from data_pipeline.downloader import download_data
from data_pipeline.processor import process_data
from data_pipeline.db_updater import update_database

async def run_pipeline():
    try:
        print("Starting data pipeline...")
        await download_data()
        process_data()
        await update_database()
        print("Pipeline executed successfully.")
        return "Pipeline executed successfully."
    except Exception as e:
        print(f"Error in pipeline: {e}")
        return str(e)