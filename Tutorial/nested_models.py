from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator,computed_field
from typing import List,Dict,Optional,Annotated





class Address(BaseModel):
    city:str
    state:str
    pin:str



class Patient(BaseModel):
    #The fields are required by1 default'a
    name:str
    gender: str
    age : int
    address: Address


address_dict={'city':'gurgaon','state':'haryana','pin':'122001'}

address1=Address(**address_dict)

patient_dict={'name':'Anoop','gender':'male','age':35,'address':address1}

patient1=Patient(**patient_dict)
    
    
print(patient1.address) 


temp=patient1.model_dump()

print(temp)
print(type(temp))

temp=patient1.model_dump_json()
print(temp)
print(type(temp))


temp=patient1.model_dump(include=['name','age'],exclude=['gender'])

print(temp)
print(type(temp))


temp=patient1.model_dump(include=['name','age'],exclude={'address':['state']})

print(temp)
print(type(temp))

temp=patient1.model_dump(include=['name','age'],exclude={'address':['state']})

print(temp)
print(type(temp))


temp=patient1.model_dump(exclude_unset=True)  #When setting a model if we have default values are set, then that would not be exported

print(temp)
print(type(temp))