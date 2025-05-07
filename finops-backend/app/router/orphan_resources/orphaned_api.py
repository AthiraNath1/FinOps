import logging

from fastapi import APIRouter, Depends, HTTPException, status
from router.authentication.auth_api import verify_token

# from finx_engine.libraries.authenticaion.authentication import get_logged_in_user
from router.orphan_resources.schemas import DeleteResourceModel
from router.orphan_resources.orphaned_resource import (
    OrphanedResources,
    delete_resources_by_ids,
    generate_orphan_resources,
)

router = APIRouter(
    tags=["Orphan Resources"]
)

module_name = "Orphaned Resources"


@router.get("/azure/orphan_resources", status_code=status.HTTP_200_OK)
def get_orphan_resources( integration_name:str,subscription_id: str,current_user: str = Depends(verify_token)):
    if current_user:
        resources: list[OrphanedResources] = generate_orphan_resources(
            integration_name,
            subscription_id
        )
        response_data = []
        if resources:
            response_data = [
                {
                    "resource_type": res.resource_type,
                    "resource_name": res.resource_name,
                    "resource_id": res.resource_id,
                    "resource_group": res.resource_group,
                    "location": res.location,
                    "cost": res.cost,
                    "orphaned_cost": res.orphaned_cost,
                }
                for res in resources
            ]
        return response_data


@router.delete(
    "/azure/delete_orphan_resources", status_code=status.HTTP_204_NO_CONTENT
)
def delete_orphan_resources(request_body: DeleteResourceModel,current_user: str = Depends(verify_token)):
    if current_user:
        resource_ids = request_body.resource_id
        integration_name = request_body.integration_name
        subscription_id = request_body.subscription_id

        try:
            response = delete_resources_by_ids(
                resource_ids, integration_name, subscription_id
            )

        except Exception as e:
            logging.exception("this is Exception mode")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            ) from e

        else:
            return response