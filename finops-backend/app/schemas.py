from pydantic import BaseModel  
from typing import List
import sys
sys.dont_write_bytecode = True

class User(BaseModel):
    username: str
    client_id: str
    client_secret: str
    tenant_id: str

class UserLogin(BaseModel):
    username: str
    finops_id: str

class DeleteResourceModel(BaseModel):
    resource_id: List[str]
    subscription_id: str
    finops_id:str

class costApiClass(BaseModel):
    subscription_id: str
    finops_id: str
    from_date: str
    to_date: str

class subscriptionListApiClass(BaseModel):
    finops_id: str

class recommendationData(BaseModel):
    finops_id: str
    subscription_id:str
    rec_id: List[str]