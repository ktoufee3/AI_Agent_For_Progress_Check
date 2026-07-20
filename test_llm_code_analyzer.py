from SMS_Project_Analyzers.llm_code_analyzer import LLMCodeAnalyzer


files = [
    {
        "path": "myapp/models.py",
        "content": """
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=250)
"""
    }
]


project_context = [
    "Project Setup",
    "Authentication",
    "Student Management",
    "Teacher Management",
    "Attendance",
    "Fees",
    "Results"
]


result = LLMCodeAnalyzer().analyze(
    files,
    project_context
)


print(result)