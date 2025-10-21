from pydantic import BaseModel,EmailStr,AnyUrl,Field
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):
    #The fields are required by default'a
    name:Annotated[str,Field(max_length=50,title='Name of the Patient',description='Give the name of the patient in less than 50 chars',examples=['Anoop','Nithish]'])]
    email: EmailStr #Custom data types from pydantic
    linked_in_url:AnyUrl
    age: int =Field(gt=0)
    weight:Annotated[float,Field(gt=0,lt=120,strict=True)] #greater than and less than 120, when strict =True type conversion doesnot happen
    married: bool =None
    allergies: Annotated[Optional[List[str]],Field(default=None,max_length=5)] #two level validation and the default value is none
    contact_details:Dict[str,   str] #two level validation

def insert_patient_data(patient:Patient):
    
    print(patient.name)
    print(patient.age)
    print(patient.email)
    # print(patient.allergies)
    print(patient.linked_in_url)
    print(patient.married)
    print('insterted into database')

patient_info={'name':'Anoop','email':'abc@gmail.com','linked_in_url':'http://linkedin.com','age':30,'weight':75.2,'contact_details':{'phone':'2345232'}}


patient1 = Patient(**patient_info)

insert_patient_data(patient1)