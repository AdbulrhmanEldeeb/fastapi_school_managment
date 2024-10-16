import sqlite3
import os
from routes.schemes import Student
from fastapi import HTTPException

class ManageStudent: 
    def __init__(self, db_dir_path: os.path = ''):
        """Initialize with the path to the database directory."""
        self.db_dir_path = db_dir_path
      
    def db_get_all_data(self):
        """Retrieve all student data from the database."""
        try: 
            # Connect to the SQLite database
            with sqlite3.connect(os.path.join(self.db_dir_path, 'studentsdb.db')) as conn:
                cursor = conn.cursor()
                
                # Fetch all student records
                all_data = cursor.execute('SELECT * FROM students').fetchall()
                all_data_list = []
                
                # Convert the fetched data into a list of dictionaries
                for record in all_data:
                    all_data_list.append(dict(zip(("id", "name", "grade"), record)))
                
                # Return the list of student data
                return all_data_list    
        except sqlite3.Error as e: 
            # Raise HTTP exception if a database error occurs
            raise HTTPException(status_code=404, detail=f"Database error: {e}")
        
    def db_get_student_data(self, student_id):
        """Fetch student data by student ID."""
        try:
            # Connect to the SQLite database
            with sqlite3.connect(os.path.join(self.db_dir_path, 'studentsdb.db')) as conn:
                cursor = conn.cursor()
                
                # Fetch student record by ID
                student = cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
                
                # Raise exception if no student is found
                if student is None:
                    raise HTTPException(status_code=404, detail=f"No student found with ID {student_id}.")
                
                # Convert the result to a dictionary and return as a Student object
                student_dict = dict(zip(("id", "name", "grade"), student))
                return Student(id=int(student_dict['id']), name=student_dict['name'], grade=student_dict['grade'])
        except sqlite3.Error as e:
            # Raise HTTP exception in case of database error
            raise HTTPException(status_code=404, detail=f"Database error: {e}")
        
    def db_add_student(self, student):
        """Add a new student to the database."""
        id = student['id']
        name = student['name']
        grade = student['grade']

        try:
            # Connect to the SQLite database
            with sqlite3.connect(os.path.join(self.db_dir_path, 'studentsdb.db')) as conn:
                cursor = conn.cursor()
                
                # Create the students table if it doesn't exist
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY,
                        name VARCHAR(20) NOT NULL,
                        grade INTEGER NOT NULL
                    )
                """)
                
                # Insert new student record into the table
                cursor.execute("INSERT INTO students (id, name, grade) VALUES (?, ?, ?)", (id, name, grade))
                
                # Return success message
                return f"Student with ID {id} added successfully."
        except sqlite3.IntegrityError:
            # Raise HTTP exception if student ID already exists (IntegrityError)
            raise HTTPException(status_code=400, detail=f"Error: Student with ID {id} already exists.")
        except sqlite3.Error as e:
            # Raise HTTP exception for other database errors
            raise HTTPException(status_code=404, detail=f"Database error: {e}")

    def db_update_student(self, student):
        """Update existing student information."""
        id = student['id']
        name = student['name']
        grade = student['grade']
        
        try:
            # Connect to the SQLite database
            with sqlite3.connect(os.path.join(self.db_dir_path, 'studentsdb.db')) as conn:
                cursor = conn.cursor()
                
                # Update student record based on ID
                cursor.execute("UPDATE students SET name = ?, grade = ? WHERE id = ?", (name, grade, id))
                
                # Check if any rows were updated, raise exception if none
                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail=f"No student found with ID {id}.")
                
                # Return success message
                return f"Student with ID {id} updated successfully."
        except sqlite3.Error as e:
            # Raise HTTP exception in case of database error
            raise HTTPException(status_code=404, detail=f"Database error: {e}")

    def db_delete_student(self, student_id):
        """Delete a student from the database by ID."""
        try:
            # Connect to the SQLite database
            with sqlite3.connect(os.path.join(self.db_dir_path, 'studentsdb.db')) as conn:
                cursor = conn.cursor()
                
                # Delete student record by ID
                cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
                
                # Check if any rows were deleted, raise exception if none
                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail=f"No student found with ID {student_id}.")
                
                # Return success message
                return f"Student with ID {student_id} deleted successfully."
        except sqlite3.Error as e:
            # Raise HTTP exception in case of database error
            raise HTTPException(status_code=404, detail=f"Database error: {e}")
