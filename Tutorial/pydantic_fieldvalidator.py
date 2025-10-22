from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator
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

    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        valid_domains=['hdfc.com','icici.com']
        domain_name=value.split("@")[-1]

        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')

        return value
    @field_validator('name')
    @classmethod
    def transformed_name(cls,name):
        return name.upper()
    

    @field_validator('age',mode='before') #this wiill compare gefore type cohearsion  eg '30' checked before changing to 30
    @classmethod
    def validate_age(cls,value):
        if 0<value<100:
            return value
        raise ValueError('The value of age should be b/w 0 & 100')
def insert_patient_data(patient:Patient):
    
    print(patient.name)
    print(patient.age)
    print(patient.email)
    # print(patient.allergies)
    print(patient.linked_in_url)
    print(patient.married)
    print('insterted into database')

patient_info={'name':'Anoop','email':'abc@hdfc.com','linked_in_url':'http://linkedin.com','age':'30','weight':75.2,'contact_details':{'phone':'2345232'}}


patient1 = Patient(**patient_info)

insert_patient_data(patient1) 