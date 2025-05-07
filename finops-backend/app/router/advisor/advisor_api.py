from fastapi import APIRouter, Depends, HTTPException, status
from router.authentication.auth_api import verify_token

# from finx_engine.libraries.authenticaion.authentication import get_logged_in_user
from router.advisor.schemas import RecommendationData
from router.advisor.advisor_operation import (
    active_data,
    exclude_recommendation,
    ignored_data,
    include_recommendatiaton,
    send_to_db,
)


router = APIRouter(tags=["Advisor"])

module_name = "Advisor"


@router.get("/azure/advisor", status_code=status.HTTP_200_OK)
def get_total_cost(integration_name: str, subscription_id: str,current_user: str = Depends(verify_token)):
    if current_user:
        data = send_to_db(integration_name, subscription_id)
        if data is not None:
            return data

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fetch data,try again",
        )


@router.get("/active_data", status_code=status.HTTP_200_OK)
def get_active_recommendation(integration_name: str, subscription_id: str | None = None,current_user: str = Depends(verify_token)):
    if current_user:
        all_active_recommendation_data = active_data(integration_name=integration_name)
        if all_active_recommendation_data:
            return [
                data
                for data in all_active_recommendation_data
                if data.subscription_id == subscription_id
            ]

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fetch data,try again",
        )


@router.get("/ignore_data", status_code=status.HTTP_200_OK)
def get_ignored_recommendation(integration_name: str, subscription_id: str | None = None,current_user: str = Depends(verify_token)):
    if current_user:
        all_excluded_recommendation_data = ignored_data(integration_name)
        if all_excluded_recommendation_data:
            return [
                data
                for data in all_excluded_recommendation_data
                if data.subscription_id == subscription_id
            ]
        return []
        # raise HTTPException(
        #     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #     detail="Unable to fetch data,try again",
        # )


@router.post("/exclude_recommendations")
def exclude_recommendations(exc_rec: RecommendationData, integration_name,current_user: str = Depends(verify_token)):
    if current_user:
        data = exclude_recommendation(
            recommendation_id=exc_rec.recommendation_id, integration_name=integration_name
        )
        if data:
            return data
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fetch data,try again",
        )


@router.post("/include_recommendations")
def active_recommendations(inc_rec: RecommendationData, integration_name,current_user: str = Depends(verify_token)):
    if current_user:
        data = include_recommendatiaton(
            recommendation_id=inc_rec.recommendation_id, integration_name=integration_name
        )
        if data:
            return data
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to fetch data,try again",
        )


