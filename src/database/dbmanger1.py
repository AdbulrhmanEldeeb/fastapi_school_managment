import sqlite3
import os
from fastapi import HTTPException
from routes.schemes import Student
from typing import List, Dict

class ManageStudent:
    def __init__(self, db_dir_path: str = ''):
        """Initialize the manager with the database directory path."""
        self.db_path = os.path.join(db_dir_path, 'studentsdb.db')
        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self):
        """Create the students table if it does not already exist."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY,
                        name VARCHAR(20) NOT NULL,
                        grade INTEGER NOT NULL
                    )
                """)
        except sqlite3.Error as e:
            raise HTTPException(status_code=500, detail=f"Database initialization error: {e}")

    def get_all_students(self) -> List[Dict[str, any]]:
        """Retrieve all students from the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                all_data = cursor.execute('SELECT * FROM students').fetchall()
                return [dict(zip(("id", "name", "grade"), record)) for record in all_data]
        except sqlite3.Error as e:
            raise HTTPException(status_code=500, detail=f"Database error: {e}")

    def get_student_by_id(self, student_id: int) -> Student:
        """Fetch a single student by their ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                student = cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
                if student is None:
                    raise HTTPException(status_code=404, detail=f"No student found with ID {student_id}.")
                student_dict = dict(zip(("id", "name", "grade"), student))
                return Student(id=int(student_dict['id']), name=student_dict['name'], grade=student_dict['grade'])
        except sqlite3.Error as e:
            raise HTTPException(status_code=500, detail=f"Database error: {e}")

    def add_student(self, student: Student) -> str:
        """Add a new student to the database."""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO students (id, name, grade) VALUES (?, ?, ?)",
                               (student['id'], student['name'], student['grade']))
            return f"Student with ID {student['id']} added successfully."
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail=f"Student with ID {student['id']} already exists.")
        except sqlite3.Error as e:
            raise HTTPException(status_code=500, detail=f"Database error: {e}")

    def update_student(self, student: Student) -> str:
        """Update an existing student's information."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE students SET name = ?, grade = ? WHERE id = ?",
                               (student['name'], student['grade'], student['id']))
                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail=f"No student found with ID {student['id']}.")
            return f"Student with ID {student['id']} updated successfully."
        except sqlite3.Error as e:
            raise HTTPException(status_code=500, detail=f"Database error: {e}")

    def delete_student(self, student_id: int) -> str:
        """Delete a student by their ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail=f"No student found with ID {student_id}.")
            return f"Student with ID {student_id} deleted successfully."
        except sqlite3.Error as e:
            raise HTTPException(status_code=500, detail=f"Database error: {e}")

# Usage Example:
# db_manager = StudentDatabaseManager(db_dir_path='path_to_db_directory')
# print(db_manager.get_all_students())
