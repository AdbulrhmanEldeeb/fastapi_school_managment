from fastapi import APIRouter, HTTPException, Query
from .schemes import Student
from database import ManageStudent  
import os
from typing import Annotated   
# Define the base directory of the current file
base_dir = os.path.dirname(__file__)
# Define the relative path to the database directory
relative_db_path = os.path.join(base_dir, '..', 'database')
# db_dir_path points to the database location
db_dir_path = relative_db_path

# Initialize the APIRouter to handle routes for managing students
base_router = APIRouter() 

@base_router.get('/data', response_model=Student)
async def get_data(id: int = Query(..., gt=0, description="identifier of student")) -> Student:
    """
    Retrieve student data by ID.
    If no student is found, an HTTP 404 exception is raised.
    """
    student = ManageStudent(db_dir_path=db_dir_path).get_student_by_id(student_id=id)
    if student is None: 
        raise HTTPException(status_code=404, detail='this id is not in data')

    return student

@base_router.post('/add_student', response_model=Student)
async def add_student(student_data: Student) -> Student: 
    """
    Add a new student to the database.
    Accepts a Student object and returns the same object on success.
    """
    ManageStudent(db_dir_path=db_dir_path).add_student(student=student_data.dict())
    return student_data
    
@base_router.put('/update_student', response_model=Student)
async def update_student(updated_student_data: Student) -> Student:
    """
    Update existing student information in the database.
    Accepts a Student object with updated data and returns the updated object.
    """
    ManageStudent(db_dir_path=db_dir_path).update_student(student=updated_student_data.dict())
    return updated_student_data

@base_router.delete('/delete_student')
async def delete_student(id: Annotated[int ,Query( gt=0, description="identifier of student")]):
    """
    Delete a student from the database using their ID.
    If the student is successfully deleted, return a success message.
    """
    ManageStudent(db_dir_path=db_dir_path).delete_student(student_id=id)
    return {
        'message': f"student with id {id} was deleted successfully"
    }
