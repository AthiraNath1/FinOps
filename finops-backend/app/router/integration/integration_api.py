import base64
import json

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from router.authentication.auth_api import verify_token
from core_dependencies.database import get_db
# from finx_engine.libraries.authenticaion.authentication import (
#     get_logged_in_user,
# )
from router.integration.schemas import (
    IntergrationCreate,
    IntegrationCreateModel,
    PlatformType
)
from router.integration.db_operation import db_integration
import os
os.environ["AZURE_CORE_SKIP_CERT_VALIDATION"] = "true"
router = APIRouter(
    tags=["Integration API"]
)

credential = DefaultAzureCredential()
key_vault_url = "https://demo-key-vault2.vault.azure.net/"
secret_client = SecretClient(vault_url=key_vault_url, credential=credential)


@router.get("/list")
def list(
    platform: PlatformType,
    user_email: str = Depends(verify_token),
    db=Depends(get_db),
):
    return db_integration.list_by_user(db=db, user_email=user_email, platform=platform)



@router.post("/create")
def create(
    integration: IntergrationCreate,
    db=Depends(get_db)
):
    # if integration.user_email != user_email:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN, detail="Cannot create for the user"
    #     )

    if integration.platform.value == "AZURE":
        key_valut_payload = {
            "client_id": integration.client_id,
            "client_secret": integration.client_secret,
            "tenant_id": integration.tenant_id,
        }
    elif integration.platform.value == "AWS":
        key_valut_payload = {
            "access_key_id": integration.client_id,
            "secret_access_key": integration.client_secret,
        }

    base64_encoded = base64.b64encode(
        json.dumps(key_valut_payload).encode("utf-8")
    ).decode("utf-8")
    print(base64_encoded)
    secret_client.set_secret(name=integration.integration_name, value=base64_encoded)
    return db_integration.create(
        db,
        IntegrationCreateModel(
            integration_name=integration.integration_name,
            user_email= integration.user_email,
            client_id=integration.client_id,
            client_secret=integration.client_secret,
            platform=integration.platform,
        ),
    )