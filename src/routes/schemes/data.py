from pydantic import BaseModel  


class Student(BaseModel): 
    id   : int 
    name : str 
    grade: int 
    class Config:
        extra = "forbid" 