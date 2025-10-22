from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,computed_field
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):
    #The fields are required by default'a
    name:str
    email: EmailStr 
    linked_in_url:AnyUrl
    age: int =Field(gt=0)
    weight:float
    height:float
    married: bool =None
    allergies: List[str]=None
    contact_details:Dict[str,   str] 

    @computed_field
    @property
    def calculate_bmi(self)->float:
        bmi=round(self.weight/self.height**2,2)
        return bmi
    
    
def insert_patient_data(patient:Patient):
    
    print(patient.name)
    print(patient.age)
    print(patient.email)
    # print(patient.allergies)
    print(patient.linked_in_url)
    print(patient.married)
    print(patient.calculate_bmi)
    print('insterted into database')



patient_info={'name':'Anoop','email':'abc@hdfc.com','linked_in_url':'http://linkedin.com','age':'30','weight':75.2,'height':1.70,  'contact_details':{'phone':'2345232'}}


patient1 = Patient(**patient_info)

insert_patient_data(patient1)