from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,model_validator
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):
    #The fields are required by default'a
    name:str
    email: EmailStr 
    linked_in_url:AnyUrl
    age: int =Field(gt=0)
    weight:float
    married: bool =None
    allergies: List[str]=None
    contact_details:Dict[str,   str] 

    @model_validator(mode='after')
    def validate_emergency_contact(cls,model):
        if model.age>60 and 'emergency' not in model.contact_details:
            raise ValueError('Person above age 60 should have an emergency conatact')

   
def insert_patient_data(patient:Patient):
    
    print(patient.name)
    print(patient.age)
    print(patient.email)
    # print(patient.allergies)
    print(patient.linked_in_url)
    print(patient.married)
    print('insterted into database')

patient_info={'name':'Anoop','email':'abc@hdfc.com','linked_in_url':'http://linkedin.com','age':65,'weight':75.2,'contact_details':{'phone':'2345232','emergency':'23432'}}


patient1 = Patient(**patient_info)

insert_patient_data(patient1)