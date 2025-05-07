import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from azure.identity import ClientSecretCredential
from azure.mgmt.advisor import AdvisorManagementClient
from azure.mgmt.advisor.models import ResourceRecommendationBaseListResult
from sqlmodel import Session

from core_dependencies.database import get_db
from router.advisor.schemas import (
    AdvisorModel,
    BaseAdvisorModel,
    TransformedCache,
)
from router.advisor.db_operation import db_advisor, db_exclude_advisor
from router.user_details.user_details import (
    get_client_by_integration_name,
)


def collect_cached_list_advisor_recommendation(
    integration_name: str, subscription_id: str
) -> ResourceRecommendationBaseListResult:
    try:
        client_secrets = get_client_by_integration_name(integration_name)

        credential = ClientSecretCredential(
            tenant_id=client_secrets["tenant_id"],
            client_id=client_secrets["client_id"],
            client_secret=client_secrets["client_secret"],
        )

        advisor_client = AdvisorManagementClient(
            credential=credential,
            subscription_id=subscription_id,
        )

        cached_list = advisor_client.recommendations.list()

    except Exception:
        logging.exception("this is Exception mode")
    else:
        return cached_list


def transform_cached_list(
    cached_list: ResourceRecommendationBaseListResult,
) -> list[TransformedCache]:
    try:
        res = []

        if not cached_list:
            return []

        for cached_list_iterator in cached_list:
            monthly_cost_savings = 0
            savings_currency = ""
            recommendation = ""

            # Additional field computations for 'cost' category
            if (
                cached_list_iterator.category == "Cost"
                and cached_list_iterator.extended_properties is not None
            ):
                monthly_cost_savings = cached_list_iterator.extended_properties.get(
                    "savingsAmount",
                    0,
                )
                savings_currency = cached_list_iterator.extended_properties.get(
                    "savingsCurrency",
                    "",
                )
                recommendation = cached_list_iterator.extended_properties.get(
                    "recommendationMessage",
                    "",
                )

            rest = (cached_list_iterator.resource_metadata.resource_id).split("/")
            ## Recommendation for resource_group / resource

            res.append(
                BaseAdvisorModel(
                    recommendation_id=cached_list_iterator.id,
                    category=cached_list_iterator.category,
                    impact=cached_list_iterator.impact,
                    impacted_field=cached_list_iterator.impacted_field,
                    problem=cached_list_iterator.short_description.problem,
                    solution=cached_list_iterator.short_description.solution,
                    resource_id=cached_list_iterator.resource_metadata.resource_id,
                    source=cached_list_iterator.resource_metadata.source,
                    resource_group=rest[4] if len(rest) > 3 else "",
                    resource=rest[-1] if len(rest) > 3 else "",
                    monthly_cost_savings=monthly_cost_savings,
                    savings_currency=savings_currency,
                    recommendation=recommendation,
                )
            )

    except Exception:
        logging.exception("error occured")
    else:
        return res


def generate_data(
    subscription_id: str, integration_name: str
) -> list[TransformedCache]:
    cached_advisor_list = collect_cached_list_advisor_recommendation(
        subscription_id=subscription_id, integration_name=integration_name
    )
    return transform_cached_list(cached_advisor_list)


def send_to_db(
    integration_name: str, subscription_id: str, db: Session = next(get_db())
) -> str:
    values = generate_data(subscription_id, integration_name)
    for value in values:
        db_advisor.create(
            db,
            AdvisorModel(
                finops_id=integration_name,
                subscription_id=str(subscription_id),
                **value.model_dump(),
            ),
        )
    if values:
            return values

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Unable to fetch data,try again",
        )


def exclude_recommendation(
    recommendation_id: str, integration_name: str, db: Session = next(get_db())
) -> str:
    db_exclude_advisor.add_exlude_advisor_data(
        db=db, recommendation_id=recommendation_id, integration_name=integration_name
    )

    return {
        "recommendation_id": recommendation_id,
        "recommendation_moved_to_ignored": True,
    }


def include_recommendatiaton(
    recommendation_id: str, integration_name: str, db: Session = next(get_db())
) -> str:
    db_exclude_advisor.delete_by_rec_id(
        db, recommendation_id=recommendation_id, integration_name=integration_name
    )

    return {
        "recommendation_id": recommendation_id,
        "recommendation_moved_to_active": True,
    }


def ignored_data(
    integration_name: str, db: Session = next(get_db())
) -> List[AdvisorModel]:
    return db_exclude_advisor.query_by_integration_name(db, integration_name)


def active_data(
    integration_name: str, db: Session = next(get_db())
) -> List[AdvisorModel]:
    all_data = db_advisor.query_by_integration_name(db, integration_name)
    ignored_data = db_exclude_advisor.query_by_integration_name(db, integration_name)
    print(ignored_data)
    return [
        data
        for data in all_data
        if data.recommendation_id
        not in (data.recommendation_id for data in ignored_data)
    ]