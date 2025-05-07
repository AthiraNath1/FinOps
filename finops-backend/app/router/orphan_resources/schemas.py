from pydantic import BaseModel, constr
from typing import List

class DeleteResourceModel(BaseModel):
    resource_id: List[str]
    integration_name: str
    subscription_id: str