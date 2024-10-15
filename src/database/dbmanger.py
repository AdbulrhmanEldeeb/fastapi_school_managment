import sqlite3
import os 
from routes.schemes import Student
from fastapi import HTTPException

def db_get_all_data(db_dir_path=''):
    try: 
        with sqlite3.connect(os.path.join(db_dir_path,'studentsdb.db')) as conn:
            cursor = conn.cursor()
            all_data=cursor.execute('SELECT *  FROM students').fetchall()
            all_data_list=[]
            for record in all_data:
                all_data_list.append(dict(zip(("id","name","grade"),record)))
            return all_data_list    
    except sqlite3.Error as e : 
        raise HTTPException(status_code=404,detail= f"database error : {e}")

def db_get_student_data(student_id,db_dir_path=''):
    """Fetch student data by ID."""
    try:
        with sqlite3.connect(os.path.join(db_dir_path,'studentsdb.db')) as conn:
            cursor = conn.cursor()
            student = cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
            if student is None:
                raise HTTPException(status_code=404,detail= f"No student found with ID {student_id}.")
            student_dict=dict(zip(("id","name","grade"),student))
            student_dict=Student(id=int(student_dict['id']),name=student_dict['name'],grade=student_dict['grade'])
            return student_dict
    except sqlite3.Error as e:
        raise HTTPException(status_code=404,detail= f"Database error: {e}")
def db_add_student(student,db_dir_path=''):
    """Add a new student to the database."""
    id = student['id']
    name = student['name']
    grade = student['grade']

    try:
        with sqlite3.connect(os.path.join(db_dir_path,'studentsdb.db')) as conn:
            cursor = conn.cursor()
            # Create the table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(20) NOT NULL,
                    grade INTEGER NOT NULL
                )
            """)
            # Insert student data into the table
            cursor.execute("INSERT INTO students (id, name, grade) VALUES (?, ?, ?)", (id, name, grade))
            return f"Student with ID {id} added successfully."
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=404, detail=f"Error: Student with ID {id} already exists.")
    except sqlite3.Error as e:
        raise HTTPException(status_code=404,detail=f"Database error: {e}")

def db_update_student(student,db_dir_path=''):
    """Update existing student information."""
    id = student['id']
    name = student['name']
    grade = student['grade']
    
    try:
        with sqlite3.connect(os.path.join(db_dir_path,'studentsdb.db')) as conn:
            cursor = conn.cursor()
            # Use a correct SQL statement for updating
            cursor.execute("UPDATE students SET name = ?, grade = ? WHERE id = ?", (name, grade, id))
            if cursor.rowcount == 0:
                raise  HTTPException(status_code=404,detail=f"No student found with ID {id}.")
            return f"Student with ID {id} updated successfully."
    except sqlite3.Error as e:
        raise  HTTPException(status_code=404,detail=f"Database error: {e}")

def db_delete_student(student_id,db_dir_path=''):
    """Delete a student from the database by ID."""
    try:
        with sqlite3.connect(os.path.join(db_dir_path,'studentsdb.db')) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404,detail=f"No student found with ID {student_id}.")
            return f"Student with ID {student_id} deleted successfully."
    except sqlite3.Error as e:
        raise HTTPException(status_code=404, detail=f"Database error: {e}")

# Test the functions
# print(db_add_student({"id":8,"name":"samy","grade":6}))  # Adjust ID as necessary for testing
# print(dict(zip(("id","name","grade"),db_get_all_data()[0])))
# print(db_get_all_data())