from database import engine, Base
from model import Student

Base.metadata.create_all(bind=engine)

print("Student table created successfully!")