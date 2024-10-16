import sqlite3
import os 
from routes.schemes import Student
from fastapi import HTTPException

class ManageStudent: 
    def __init__(self,db_dir_path:os.path=''):
        self.db_dir_path=db_dir_path 
      

    def db_get_all_data(self):
        try: 
            with sqlite3.connect(os.path.join(self.db_dir_path,'studentsdb.db')) as conn:
                cursor = conn.cursor()
                all_data=cursor.execute('SELECT *  FROM students').fetchall()
                all_data_list=[]
                for record in all_data:
                    all_data_list.append(dict(zip(("id","name","grade"),record)))
                return all_data_list    
        except sqlite3.Error as e : 
            raise HTTPException(status_code=404,detail= f"database error : {e}")
        

    def db_get_student_data(self,student_id):
        """Fetch student data by ID."""
        try:
            with sqlite3.connect(os.path.join(self.db_dir_path,'studentsdb.db')) as conn:
                cursor = conn.cursor()
                student = cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
                if student is None:
                    raise HTTPException(status_code=404,detail= f"No student found with ID {student_id}.")
                student_dict=dict(zip(("id","name","grade"),student))
                student_dict=Student(id=int(student_dict['id']),name=student_dict['name'],grade=student_dict['grade'])
                return student_dict
        except sqlite3.Error as e:
            raise HTTPException(status_code=404,detail= f"Database error: {e}")
        
    def db_add_student(self,student):
        """Add a new student to the database."""
        id = student['id']
        name = student['name']
        grade = student['grade']

        try:
            with sqlite3.connect(os.path.join(self.db_dir_path,'studentsdb.db')) as conn:
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
        # IntegrityError status code 400 not 404 
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail=f"Error: Student with ID {id} already exists.")
        except sqlite3.Error as e:
            raise HTTPException(status_code=404,detail=f"Database error: {e}")

    def db_update_student(self,student):
        """Update existing student information."""
        id = student['id']
        name = student['name']
        grade = student['grade']
        
        try:
            with sqlite3.connect(os.path.join(self.db_dir_path,'studentsdb.db')) as conn:
                cursor = conn.cursor()
                # Use a correct SQL statement for updating
                cursor.execute("UPDATE students SET name = ?, grade = ? WHERE id = ?", (name, grade, id))
                if cursor.rowcount == 0:
                    raise  HTTPException(status_code=404,detail=f"No student found with ID {id}.")
                return f"Student with ID {id} updated successfully."
        except sqlite3.Error as e:
            raise  HTTPException(status_code=404,detail=f"Database error: {e}")

    def db_delete_student(self,student_id):
        """Delete a student from the database by ID."""
        try:
            with sqlite3.connect(os.path.join(self.db_dir_path,'studentsdb.db')) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404,detail=f"No student found with ID {student_id}.")
                return f"Student with ID {student_id} deleted successfully."
        except sqlite3.Error as e:
            raise HTTPException(status_code=404, detail=f"Database error: {e}")


        