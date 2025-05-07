from datetime import datetime
from enum import Enum
from uuid import uuid4

from azure.identity import ClientSecretCredential
from pydantic import UUID4
from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel


class PlatformType(Enum):
    AZURE = "AZURE"
    AWS = "AWS"
    GCP = "GCP"
    ON_PREMISE = "ON_PREMISE"


class IntegrationBaseModel(SQLModel):
    integration_name: str = Field(max_length=20, unique=True)
    user_email: str
    created_at: datetime = Field(
        default=datetime.now(),
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
    )
    modified_at: datetime = Field(
        default=datetime.now(),
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
    )
    platform: PlatformType


class IntegrationCreateModel(IntegrationBaseModel):
    id: UUID4 = Field(default_factory=uuid4, primary_key=True)


class IntegrationUpdateModel(IntegrationCreateModel):
    pass


class IntegrationResponseModel(IntegrationBaseModel):
    id: UUID4

    
class IntergrationCreate(IntegrationBaseModel):
    client_id: str
    client_secret: str
    tenant_id: str | None

    def get_client_secret_cred(self):
        return ClientSecretCredential(
            tenant_id=self.tenant_id,
            client_id=self.client_id,
            client_secret=self.client_secret,
        )