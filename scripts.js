const API_URL = 'http://localhost:8000';

async function getStudent() {
    const id = document.getElementById('student-id').value;
    try {
        const response = await fetch(`${API_URL}/data?id=${id}`);
        const student = await response.json();
        displayStudent(student);
    } catch (error) {
        alert('Student not found.');
    }
}

async function addStudent() {
    const student = {
        id: parseInt(document.getElementById('student-id').value),
        name: document.getElementById('student-name').value,
        grade: parseInt(document.getElementById('student-grade').value),
    };

    try {
        const response = await fetch(`${API_URL}/add_student`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(student),
        });
        const newStudent = await response.json();
        alert('Student added successfully');
        displayStudent(newStudent);
    } catch (error) {
        alert('Error adding student.');
    }
}

async function updateStudent() {
    const id = parseInt(document.getElementById('student-id').value);
    const student = {
        id: id,
        name: document.getElementById('student-name').value,
        grade: parseInt(document.getElementById('student-grade').value),
    };

    try {
        const response = await fetch(`${API_URL}/update_student/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(student),
        });
        const updatedStudent = await response.json();
        alert('Student updated successfully');
        displayStudent(updatedStudent);
    } catch (error) {
        alert('Error updating student.');
    }
}

async function deleteStudent() {
    const id = parseInt(document.getElementById('student-id').value);

    try {
        await fetch(`${API_URL}/delete_student/${id}`, {
            method: 'DELETE',
        });
        alert('Student deleted successfully');
        clearDisplay();
    } catch (error) {
        alert('Error deleting student.');
    }
}

function displayStudent(student) {
    const studentsList = document.getElementById('students-list');
    studentsList.innerHTML = `<p>ID: ${student.id}</p><p>Name: ${student.name}</p><p>Grade: ${student.grade}</p>`;
}

function clearDisplay() {
    document.getElementById('students-list').innerHTML = '';
}
