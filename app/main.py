
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import SessionLocal
from model import Student

app = FastAPI()

students = []


# Database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Student model for database input
class StudentCreate(BaseModel):
    name: str
    email: str
    department: str
    graduation_year: int


# Add student to PostgreSQL
@app.post("/db/students")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):

    new_student = Student(
        name=student.name,
        email=student.email,
        department=student.department,
        graduation_year=student.graduation_year
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "message": "Student added successfully",
        "student_id": new_student.id
    }


# View students from PostgreSQL
@app.get("/db/students")
def get_db_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


# Home API
@app.get("/")
def home():
    return {"message": "Campus Placement System"}


# Old CRUD using Python list
@app.post("/students")
def add_student(name: str, age: int, course: str):
    student = {
        "name": name,
        "age": age,
        "course": course
    }

    students.append(student)

    return {"message": "Student added successfully"}


@app.get("/students")
def get_students():
    return students


@app.put("/students/{student_id}")
def update_student(student_id: int, name: str):
    if student_id < 0 or student_id >= len(students):
        return {"message": "Student not found"}

    students[student_id]["name"] = name

    return {"message": "Student updated"}


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id < 0 or student_id >= len(students):
        return {"message": "Student not found"}

    students.pop(student_id)

    return {"message": "Student deleted"}

