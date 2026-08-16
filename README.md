#            AI Agent for Project Progress Checking

An AI-powered agent that analyzes a Django/DRF project, tracks Git changes, evaluates module progress, and provides project status through conversational interaction.

# Features
🤖 AI-powered project progress analysis
💬 Conversational interaction with memory
🔍 Git commit and changed-file analysis
📊 Module-wise project progress tracking
🗂️ Project status and metadata retrieval
🧠 LLM-based code analysis
⚡ FastAPI-based application interface
🗄️ PostgreSQL database for project and Git tracking
🛠️ Tool-based agent architecture

# Project Structure

AI_Agent_For_Progress_Check/
│
├── SMS_Project_Analyzers/
│   ├── git_analyzer.py
│   ├── local_code_analyzer.py
│   ├── file_reader.py
│   ├── llm_code_analyzer.py
│   └── super_code_analyzer.py
│
├── database/
│   ├── db_manager.py
│   └── db_utils.py
│
├── tools/
│   ├── project_analyzer_tool.py
│   ├── project_status_tool.py
│   └── git_history_tool.py
│
├── app.py
├── llm.py
├── .env
├── config.py
├── requirements.txt
└── README.md

# Installation
Clone the repository and create/activate a virtual environment:

# Install the required packages:
pip install groq python-dotenv

# Install other project dependencies
pip install groq python-dotenv

# Run the Project
- Running the Project
python app.py