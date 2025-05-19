
# User-Facing Chat-Style RAG Agentic System

## Overview

This project is developed as part of an assignment for the AI Engineer position at Spiderweb Technologies. 
It features a **User-Facing Chat-Style RAG Agentic System** utilizing asynchronous Python programming, FastAPI, 
and a local LLM integrated with a daily-updated MySQL database. 
The system efficiently handles both chat-style interactions and database queries.

## Key Features

- **Interactive Chatbot UI**: A ReactJS-based frontend for interacting with the chatbot, located at `Project_root/Frontend/rag_frontend/public`.
- **Asynchronous Data Pipeline**: Efficient data downloading, processing, and database updates using asyncio.
- **Chat-Style Interaction**: User-friendly interface for chat interactions using a local LLM model.
- **Database Access**: Supports structured database queries and retrieves information from the daily-updated MySQL database.
- **FastAPI Integration**: Offers RESTful API endpoints for interaction.
- **Modular Code Structure**: Separates data pipeline and API logic for clarity and maintainability.

## Project Structure

```
project_root/
├── data_pipeline/
│   ├── downloader.py       # Asynchronous data download
│   ├── processor.py        # Data processing and cleaning
│   └── db_updater.py       # Updating MySQL database
├── Frontend/
│   └── rag_frontend/
│       └── public/         # ReactJS-based chatbot UI
├── main.py                 # FastAPI server with LLM and database integration
├── requirements.txt        # Dependencies
├── README.md               # Project documentation
└── .gitignore              # Ignored files and folders
```

## Installation

### Database Installation
In order to access the database, make sure to create a MySQL database named `fd_data` and a table named `federal_register`.

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/phani-x507/Retrieval-Augmented-Generation-using-Federal-Data-API.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Retrieval-Augmented-Generation-using-Federal-Data-API
   ```
3. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scriptsctivate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd Frontend/rag_frontend
   ```
2. Install frontend dependencies:
   ```bash
   npm install
   ```
3. Start the frontend server:
   ```bash
   npm start
   ```
3. Visit localhost:
   ```bash
   http://localhost:3000/
   ```

## Running the Project

1. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
2. Access the API at:
   ```
   http://localhost:8000
   ```

## Usage
- Send a POST request to the `/chat` endpoint:
```bash
curl -X POST "http://localhost:8000/chat" -d '{"query": "Show recent executive orders"}'
```

- Expected JSON response:
  ```json
  {
    "response": ["Title: Order 12345, Date: 2025-05-17"]
  }
  ```

## Screenshots
![alt text]([http://url/to/img.png](https://github.com/phani-x507/Retrieval-Augmented-Generation-using-Federal-Data-API/blob/main/Screenshots/scrsht1.png))


## Known Issues

- Nothing

## Contributing

Feel free to submit issues or pull requests. Contributions are welcome!

## Contact

For any questions or support, please reach out to Sricharan Sai Krishna Phani at [[charansri595@gmail.com](mailto:charansri595@gmail.com)].
