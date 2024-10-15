from fastapi import APIRouter , HTTPException 
from .schemes import Student 
from database import dbmanger
db_dir_path=r'F:\programing\fast_api\school_system\src\database'

# student_list=dbmanger.db_get_all_data(db_dir_path=db_dir_path)
# students=[Student(s) for s in students]
# students=[]
# for s in student_list : 
#     student=Student(id=s['id'],name=s['name'],grade=s['grade'])
#     students.append(student)

base_router=APIRouter() 

@base_router.get('/data',response_model=Student)
async def get_data(id : int) -> Student:
    student=dbmanger.db_get_student_data(student_id=id,db_dir_path=db_dir_path)
    # student=next((s for s in students if s.id==id),None)
    if student is None : 
        raise  HTTPException(status_code=404,detail='this id is not in data')

    return student

@base_router.post('/add_student',response_model=Student)
async def add_student(student_data:Student): 
    if any(s for s in students if s.id==student_data.id): 
        raise HTTPException(status_code=404,detail='this student alrady exists')
    students.append(student_data)
    return student_data 
    
@base_router.put('/update_student/{id}',response_model=Student)
async def update_student(id : int,updated_student_data:Student):
    student=next((s for s in students if s.id==id),None)
    if student is None : 
        raise  HTTPException(status_code=404,detail='this id is not in data')   
    
    index=students.index(student)
    students[index]=updated_student_data 
    students[index].id = id 
    return updated_student_data


@base_router.delete('/delete_student/{id}')
async def delete_student(id : int):
    student=next((s for s in students if s.id==id),None)
    if student is None : 
        raise HTTPException(status_code=404,detail="this student id is not in data")
    else: 
        students.remove(student)
        return {"message":"student deleted successfully"}