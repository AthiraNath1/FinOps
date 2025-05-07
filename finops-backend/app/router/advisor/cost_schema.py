from datetime import date, datetime
from uuid import uuid4

from pydantic import UUID4
from sqlmodel import Field, SQLModel


class CostBase(SQLModel):
    subscription_name: str
    resource_group_name: str
    resource_id: str
    resource_type: str
    resource_location: str
    consumed_service: str
    usage_date: date
    reservation_id: str
    reservation_name: str
    service_name: str
    service_tier: str
    billing_month: datetime
    billing_period: str
    currency: str
    cost: float


class CostBaseModel(CostBase):
    cost_id: UUID4 = Field(primary_key=True, default_factory=uuid4)
    finops_id: str


class CostApiClass(SQLModel):
    subscription_id: str
    finops_id: str
    from_date: date = Field(default=date.today())
    to_date: date = Field(default=date.today())