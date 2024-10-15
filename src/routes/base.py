from fastapi import APIRouter , HTTPException , Query 
from .schemes import Student 
from database import dbmanger
import os

db_dir_path=r'F:\programing\fast_api\school_system\src\database'

base_dir = os.path.dirname(__file__)
relative_db_path = os.path.join(base_dir, '..', 'database', 'studentsdb.db')
absolute_db_path = os.path.abspath(relative_db_path)
db_dir_path=r'src\database\studentsdb.db'
base_router=APIRouter() 

@base_router.get('/data',response_model=Student)
async def get_data(id : int=Query(...,gt=0,description="identifier of student")) -> Student:
    student=dbmanger.db_get_student_data(student_id=id,db_dir_path=db_dir_path)
    # student=next((s for s in students if s.id==id),None)
    if student is None : 
        raise  HTTPException(status_code=404,detail='this id is not in data')

    return student

@base_router.post('/add_student',response_model=Student)
async def add_student(student_data:Student)->Student: 
    dbmanger.db_add_student(student_data.dict(),db_dir_path=db_dir_path)
    return student_data 
    
@base_router.put('/update_student',response_model=Student)
async def update_student(updated_student_data:Student)-> Student:
    dbmanger.db_update_student(updated_student_data.dict(),db_dir_path=db_dir_path)
    
    return updated_student_data


@base_router.delete('/delete_student')
async def delete_student(id : int = Query(...,gt=0,description="identifier of student")):
    dbmanger.db_delete_student(id,db_dir_path=db_dir_path)
    return {
        f'message':"student with id {id} was deleted successfully"
        }