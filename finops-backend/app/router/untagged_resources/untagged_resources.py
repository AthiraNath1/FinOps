# ruff: noqa: off
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from router.authentication.auth_api import verify_token
# from finx_engine.libraries.authenticaion.authentication import get_logged_in_user
from router.untagged_resources.schemas import Tag, TagInput
from router.untagged_resources.azure_tag import (
    list_azure_untagged_resources,
    tag_azure_resources,
)


router = APIRouter(
    tags=["Untagged Resources"]
)

module_name = "Untagged Resources"


@router.get("/azure/untagged_resources", status_code=status.HTTP_200_OK)
def get_azure_untagged_resources(integration_name:str,subscription_id: str,current_user: str = Depends(verify_token)):
    if current_user:
        return list_azure_untagged_resources(
            subscription_id=subscription_id,integration_name=integration_name
        )


@router.post("/azure/tag_resources", status_code=status.HTTP_201_CREATED)
def tag_azure_untagged_resources(
    integration_name:str,subscription_id: str, resource_id: str, tags: list[Tag],current_user: str = Depends(verify_token)
):
    if current_user:
        return tag_azure_resources(
            subscription_id=subscription_id,
            integration_name=integration_name,
            resource_id=resource_id,
            tags=tags,
        )