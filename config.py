from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


db_name= os.getenv("db_name")
db_host= os.getenv("db_host")
db_port= os.getenv("db_port")
db_user= os.getenv("db_user")
db_password= os.getenv("db_password")

# Path to the Django Student Management System project
SMS_PROJECT_PATH = r"F:\BecomeDataScientist\Student_Management_System"
