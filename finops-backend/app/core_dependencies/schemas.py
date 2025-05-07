from sqlmodel import Field, SQLModel

from router.integration.schemas import IntegrationCreateModel
from router.advisor.schemas import AdvisorModel
from router.advisor.cost_schema import CostBaseModel


class Advisor(AdvisorModel, table=True):
    pass


class ExcludedAdvisor(AdvisorModel, table=True):
    pass


class User(SQLModel, table=True):
    finops_id: str = Field(primary_key=True, max_length=100)
    username: str
    client_id: str


# class Cost(CostBaseModel, table=True):
#     pass


class Integration(IntegrationCreateModel, table=True):
    pass