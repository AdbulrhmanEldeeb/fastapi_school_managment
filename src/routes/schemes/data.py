from pydantic import BaseModel  

class Student(BaseModel): 
    # Define fields for the Student model: id, name, and grade
    id   : int   # Student ID (must be an integer)
    name : str   # Student name (must be a string)
    grade: int   # Student grade (must be an integer)
    
    class Config:
        # Forbid extra fields that are not defined in the model schema
        extra = "forbid"
