from typing import Optional
from uuid import uuid4

from pydantic import UUID4, BaseModel
from sqlmodel import Field, SQLModel


class AdvisorTransform(SQLModel):
    subscription_id: str
    finops_id: str
    from_date: str
    to_date: str


class RecommendationData(SQLModel):
    recommendation_id: str


class BaseAdvisorModel(SQLModel):
    recommendation_id: str
    id: UUID4 = Field(primary_key=True, default_factory=uuid4)
    category: str
    impact: str
    impacted_field: str | None
    problem: str | None
    solution: str
    resource_id: str
    source: str | None
    resource_group: str
    resource: str
    monthly_cost_savings: str
    savings_currency: str
    recommendation: str


class TransformedCache(BaseAdvisorModel):
    pass


class AdvisorModel(BaseAdvisorModel):
    finops_id: str
    subscription_id: str | None


class AdvisorChecks(BaseModel):
    id: str
    name: str
    description: str
    category: str
    metadata: Optional[list]


class FlaggedResource(BaseModel):
    status: str
    resourceId: str
    isSuppressed: bool
    metadata: Optional[list]
    region: Optional[str]


class AdvisorCheckResults(BaseModel):
    checkId: str
    timestamp: str
    status: str
    resourcesSummary: dict
    categorySpecificSummary: dict

    flaggedResources: list[FlaggedResource]


class AdvisorCheckResult(BaseModel):
    checkId: str
    timestamp: str
    status: str
    resourcesSummary: dict
    categorySpecificSummary: dict
    flaggedResource: FlaggedResource


class ValidResult(BaseModel):
    checkId: str
    status: str
    description: str
    name: str
    category: str
    categorySpecificSummary: dict
    resourceData: dict  # combine metatdata