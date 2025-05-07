from fastapi import APIRouter, Depends, HTTPException, status

from router.user_details.operation import get_subscription_list
from router.authentication.auth_api import verify_token
router = APIRouter(
    tags=["User Details List"]
)

module_name = "UserDetails"


@router.get("/azure/subscription_list", status_code=status.HTTP_200_OK)
def get_subscription_data(integration_name: str,current_user: str = Depends(verify_token)):
    if current_user:  # This will always be True if the token is valid
        return get_subscription_list(integration_name)
    else:
        raise HTTPException(status_code=403, detail="Unauthorized access")
