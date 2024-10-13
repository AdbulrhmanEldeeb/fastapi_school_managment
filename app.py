from fastapi import FastAPI , Query  , HTTPException 
from pydantic import BaseModel 
from fastapi.middleware.cors import CORSMiddleware

class Student(BaseModel): 
    id   : int 
    name : str 
    grade: int 


students=[Student(id=1,name='ahmed',grade=3),
          Student(id=2,name='ali',grade=4),
          Student(id=3,name='maher',grade=5)]

app=FastAPI() 
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],  # يسمح بالوصول من أي مصدر. قم بتقييد هذا في الإنتاج
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
@app.get('/data',response_model=Student)
async def get_data(id : int) -> Student:
    
    student=next((s for s in students if s.id==id),None)
    if student is None : 
        raise  HTTPException(status_code=404,detail='this id is not in data')

    return student

@app.post('/add_student',response_model=Student)
async def add_student(student_data:Student): 
    if any(s for s in students if s.id==student_data.id): 
        raise HTTPException(status_code=404,detail='this student alrady exists')
    students.append(student_data)
    return student_data 
    
@app.put('/update_student/{id}',response_model=Student)
async def update_student(id : int,updated_student_data:Student):
    student=next((s for s in students if s.id==id),None)
    if student is None : 
        raise  HTTPException(status_code=404,detail='this id is not in data')   
    
    index=students.index(student)
    students[index]=updated_student_data 
    students[index].id = id 
    return updated_student_data


@app.delete('/delete_student/{id}')
async def delete_student(id : int):
    student=next((s for s in students if s.id==id),None)
    if student is None : 
        raise HTTPException(status_code=404,detail="this student id is not in data")
    else: 
        students.remove(student)
        return {"message":"student deleted successfully"}