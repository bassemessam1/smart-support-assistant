# smart-support-assistant

A FastAPI-powered AI support system that allows users to open, update, and check ticket status through natural language.The system uses:

- GPT-5 (or any OpenAI LLM)
- FastAPI web interface
- MySQL persistence
- Docker Compose for deployment
- Automatic database table creation
- Structured JSON responses using Pydantic + JSON Schema

## Features

- Natural-language ticket management using AI
- Automatically detects user intent
- Executes actions via Python backend (create/update/check ticket)
- Stores tickets in a real MySQL database
- /tickets endpoint for browsing all tickets
- HTML UI for entering prompts
- Dockerized (FastAPI + MySQL + init service)
- Auto-creates tables on startup
- Clean modular structure

## Project Structure
smart-support-assistant/
```
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
│
├── app/
│   ├── main.py          # FastAPI application
│   ├── llm.py           # GPT-5 request handler
│   ├── schemas.py       # Pydantic models + JSON schema
│   ├── tools.py         # Action functions
│   ├── database.py      # MySQL CRUD functions
│   ├── db_init.py       # Auto-create tables
│   ├── model.py         # Ticket Pydantic model
│
└── README.md
```
## Installation


1. Clone the repository

&emsp; `git clone https://github.com/bassemessam1/smart-support-assistant.git`

&emsp; `cd smart-support-assistant`

2. create .env file as shown in .env.example

3. Running with `docker compose`

&emsp; `docker compose up --build`

Expected running services:

| Service | Port |
|---------|------|
| FastAPI | 8000 |
| MySQL | 3306 |


## Accessing The Application

HTML UI:

👉 http://localhost:8000/

Browse all tickets:

👉 http://localhost:8000/tickets

API Docs:

👉 http://localhost:8000/docs

