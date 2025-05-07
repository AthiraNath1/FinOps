from fastapi import status, APIRouter, HTTPException, Depends
# from more_itertools import consume
from underutilizedResources import generate_underutilized_resources
from custom_exceptions import ResourceNotFoundError, InvalidSubscriptionError
import logging
from router.authentication.auth_api import verify_token
# from custom_logging import CustomHandler

router = APIRouter(
 tags=["Underutilized Resources"]
)

module_name = 'Underutilized Resources'


@router.get('/azure/underutilizedresources', status_code=status.HTTP_200_OK)
def get_underutilized_data( integration_name,subscription_id,current_user: str = Depends(verify_token)):
    if current_user: 
        try:
            logger = logging.getLogger(__name__)
            logger.info('inside get_underutilized_data function')
            resources = generate_underutilized_resources(
                integration_name,subscription_id,logger)
            response_data = []
            if resources:
                response_data = [
                    {
                        "resource_type": res.resource_type,
                        "resource_name": res.resource_name,
                        "resource_id": res.resource_id,
                        "resource_group": res.resource_group,
                        "location": res.location,
                        "monthly_utilization_value": res.monthly_utilization_value,
                        "metric": res.metric,
                    }
                    for res in resources
                ]
            logger.info('get_underutilized_data function executed')
            return response_data
        except ResourceNotFoundError as e:
            logger.error(f'this is ResourceNotFoundError mode {e}')
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except InvalidSubscriptionError as e:
            logger.error(f'this is InvalidSubscriptionError mode {e}')
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            logger.error(f'this is error mode {e}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An internal server error occurred")