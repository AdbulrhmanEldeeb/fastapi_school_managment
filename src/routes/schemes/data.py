from pydantic import BaseModel  
from typing import Annotated 
from fastapi import Query 
class Student(BaseModel): 
    # Define fields for the Student model: id, name, and grade
    id   : int   # Student ID (must be an integer)
    name : Annotated[str,Query(max_length=20)]   # Student name (must be a string)
    grade: Annotated[int ,Query(lt=10,gt=0)]  # Student grade (must be an integer)
    
    class Config:
        # Forbid extra fields that are not defined in the model schema
        extra = "forbid"
