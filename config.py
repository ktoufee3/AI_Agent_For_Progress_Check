from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

RETRY_GROQ_API_KEY = os.getenv("RETRY_GROQ_API_KEY")

#personal laptop
db_name= os.getenv("db_name")
db_host= os.getenv("db_host")
db_port= os.getenv("db_port")
db_user= os.getenv("db_user")
db_password= os.getenv("db_password")



# Database connection URL (alternative format)
DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


#API
API_IP=os.getenv("API_IP")
API_PORT=int(os.getenv("API_PORT"))

# Path to conversation_memory.json
CONVERSATION_MEMORY_FILE = "memory/conversation_memory.json"

# Path to the Django Student Management System project
SMS_PROJECT_PATH = r"F:\BecomeDataScientist\Student_Management_System"

# SMS_PROJECT_PATH = r"/home/toufeeque/Downloads/Student_Management_System/Student_Management_System"


# Files to ignore during code analysis
IGNORED_FILES = {
    ".gitignore",
    ".env",
    "db.sqlite3"
}

# Directories to ignore during code analysis
IGNORED_DIRECTORIES = {
    ".git",
    "venv",
    "__pycache__",
    ".idea",
    ".vscode"
}



