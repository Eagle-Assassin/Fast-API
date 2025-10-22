from fastapi import FastAPI,Path,HTTPException,Query
from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from decimal import Decimal
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal


#load the env file 
load_dotenv("test.env")

#load the env details
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST", "localhost") 
database = os.getenv("DB_NAME")
port = os.getenv("DB_PORT", 3306)  # default MySQL port
password = quote_plus(password)

#Create the sql engine
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}", echo=True)

SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()


class Patient(BaseModel):
    __tablename__ = "person_info" 
    id:Annotated[str,Field(...,description="ID of the patient",examples=['P001'])]
    name:Annotated[str,Field(...,description="Name of the patient",examples=['Nithesh'])]
    city:Annotated[str,Field(...,description="City of the patient")]
    age:Annotated[int,Field(...,gt=0,lt=120,description='Age of the patient')]
    gender:Annotated[Literal['male','female','others'],Field(...,description='Gender of the patient')]
    height:Annotated[float,Field(...,gt=0,lt=2.50,description='height of the patient in mtr')]
    weight:Annotated[float,Field(...,gt=0,description='Weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self)->float:
        bmi =self.weight/self.height**2
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return 'Underweight'
        elif self.bmi<25:
            return 'Normal'
        elif self.bmi<30:
            return 'Normal'
        else:
            return "Obese"



# Helper function to convert Decimal to float
def convert_decimals(obj):
    for row in obj:
        for k, v in row.items():
            if isinstance(v, Decimal):
                row[k] = float(v)
    return obj

#Function to load data
def load_data():
    with engine.connect() as conn:
        result=conn.execute(text("SELECT * FROM person_info;"))
    rows = [dict(row._mapping) for row in result]
    rows = convert_decimals(rows)

    return rows

#Function to check if data already exits
def load_data(value):
    with engine.connect() as conn:
        result=conn.execute(text("SELECT * FROM person_info;"))
    rows = [dict(row._mapping) for row in result]
    rows = convert_decimals(rows)


app = FastAPI()



@app.get("/")
def hello():
    return{"message":"Patient Management System API"}

@app.get("/about")
def about():
    return{"message":"A Fully Functional API to manage your patient records"}

@app.get("/view")
def view():
    data=load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str=Path(...,description='ID of the patient in the db', example="p001")):
    #load all the patients
    with engine.connect() as conn:
        result=conn.execute(text(f"SELECT name, age, city, gender,height,weight,bmi,verdict FROM person_info WHERE id = :id"),{"id":patient_id})
    rows = [dict(row._mapping) for row in result]
    rows=convert_decimals(rows)
    # print(rows)
    if len(rows)!=0:
        return(rows[0])
    raise HTTPException (status_code=404,detail= 'patient not found')

@app.get('/sort')
def sort_patients(sort_by:str = Query(...,description='Sort on the basis of height,weight or BMI'),order:str=Query('asc',description='Sort in ascending or descending order')):
    valid_fields=['height','weight','bmi']

    if sort_by not in (valid_fields):
        raise HTTPException(status_code=400,detail='Invalid field,please select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400,detail='Invalid oder ,please select between asc and desc')
    
    query = f"""SELECT name, age, city, gender, height, weight, bmi, verdict 
                FROM person_info ORDER BY {sort_by} {order.upper()}"""
    with engine.connect() as conn:
        result=conn.execute(text(query))
    rows = [dict(row._mapping) for row in result]
    rows = convert_decimals(rows)

    return(rows)

@app.post('/create')
def create_patient(patient:Patient):
    #Check if patient id is in data base
    text =f""""""

    
    


