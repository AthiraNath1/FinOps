from fastapi import APIRouter, Depends, HTTPException, status

# from finx_engine.libraries.authenticaion.authentication import get_logged_in_user
from router.networking.networking_operations import NetworkManagement
from router.authentication.auth_api import verify_token
router = APIRouter(
    tags=["Networking"]
)

module_name = "networking"


@router.get("/network_properties")
def list_public_enable_resource( integration_name:str,subscription_id: str,current_user: str = Depends(verify_token)):
    if current_user:
        try:
            rest = NetworkManagement(integration_name, subscription_id)
            data = rest.get_network()

        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error,
            ) from error
        else:
            return data