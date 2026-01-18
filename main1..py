#Making a function an API : exposing the function by setting a set of rules

# API :expose somwthing toe achieve heterogenerity

from fastapi import FastAPI # main importation


app = FastAPI() # object of fast api

@app.get('/') # then we expose this function by decorating it ( at / someone will be able to execute my function)
def test():
    return {"name" : "Steve"} # we dont use print as print works for console

@app.get("/sudh/test/dsfas/fsdfs") # This decorated function is available at this path
def test1():
    return "My name is Steve, I study at VIT Bhopal."

# At this URL im executing this particular function : this is what is done at those routes

# Now this function is exposed

##############################################################################
#api through which anyone can access student data


students = {1:"akash",2:"rohit",3:"sachin"}

# function to access student data
@app.get("/students")
def get_student():
    return students

# i dont want all the data , try to give an api where we give student id and
# it returns the name of the student


@app.get("/students/{stud_id}") # while calling api we can call data we have param as a function
def student_search(stud_id:int):
    return {"id":stud_id,"name": students[stud_id]}


#now we d like to add some data inside student dictionary
@app.get("/add_student")
def add_student(stud_id:int,name:str):
    students[stud_id] = name
    return students

#here above also we can call data we have param as a function in the URL

#########################################################################
#Post
@app.post("/add_student_diff")
def add_student_diff():
    students['new_id'] = "new_name"
    return students

#here we see an example with paramaterized variables : Here we try to use a 
#parameterized variable we do this by using pydantic class concept

#Pydantic does schema validation: whenever we send the data first the system validates
#the data type

#Pydantic class example is show below
from pydantic import BaseModel

class newdata(BaseModel):  #automatically assumed as dictionary
    stud_id:int
    name: str

@app.post('/add_student_new_value')
def add_student_new_value(newdata:newdata): #typecasting to pydantic class
    students[newdata.stud_id] = newdata.name
    return students

