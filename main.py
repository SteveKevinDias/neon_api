import os
from fastapi import FastAPI
from pydantic import BaseModel # schema validation
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()



#origins = [
#    "http://localhost",
#    "http://localhost:8080", # Common port if using Python's simple HTTP server
#    "http://127.0.0.1:8000" # If the client is served from the same origin, though usually not the case here
#]
origins = ["*"] # Allow all origins for local testing

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for local testing
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"], # Allow all headers
)

db_url = os.getenv("neon_url")

# estabalish connection to database
#install psycopyg2-binary



class Student(BaseModel): #data validation
    name:str
    id:int
    age:int

def get_connection_url():
    
    connection_string = psycopg2.connect(db_url,cursor_factory = RealDictCursor)
    return connection_string


# to save data in a file
def save_student_to_file(data):
    with open("students.txt","a") as file:
        file.write(f"{data.id},{data.name},{data.age} \n")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_home():
    with open("static/index.html") as file:
        return HTMLResponse(content=file.read())

@app.post("/students")
def create_student(stud:Student):
    save_student_to_file(stud)# directly append dont make dictionary
    return {"message":"Student data saved successfully"}

@app.post("/students/db/insert")
def store_student_in_db(student:Student):
    conn = get_connection_url() # establish connection
    cursor = conn.cursor() # create a cursor pointer
    cursor.execute("SELECT * FROM student WHERE id=%s",(student.id,))
    record = cursor.fetchone()
    if record:
        cursor.close()
        conn.close()
        return {"message":"Student with given ID already exists"}
    insert_query = "INSERT INTO student(id,name,age) VALUES (%s, %s, %s)" # Query paramaterized as strings with %s
    cursor.execute(insert_query,(student.id,student.name,student.age)) # execute the query put the arguments
    conn.commit() # commit
    cursor.close()# close pointer
    conn.close() # close connection
    return {"message":"Student data inserted in database successfully"}

@app.put("/students/db/update")
def update_student_in_db(student:Student):
    conn = get_connection_url()
    cursor = conn.cursor()
    update_query = "UPDATE student SET name=%s, age=%s WHERE id=%s"
    cursor.execute(update_query,(student.name,student.age,student.id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message":"Student data updated in database successfully"}

@app.delete("/students/db/update/{id}")
def delete_student_in_db(id:int):
    conn = get_connection_url()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student WHERE id=%s",(id,))
    record = cursor.fetchone()
    if not record:
        return {"message":"Student with given ID does not exist"}
    delete_query = "DELETE FROM student WHERE id=%s"
    cursor.execute(delete_query,(id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message":"Student data deleted from database successfully"}

#New part
@app.get("/students/db/{id}")
def get_student_in_db(id:int):
    conn = get_connection_url()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student WHERE id=%s",(id,))
    record = cursor.fetchone()
    cursor.close()
    conn.close()
    if not record:
        return {"message":"Student with given ID does not exist"}
    return record

@app.get("/students/db")
def get_all_students_in_db():
    conn = get_connection_url()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records