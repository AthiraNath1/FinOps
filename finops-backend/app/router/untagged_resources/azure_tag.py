# ERA001
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import TagsPatchResource
from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.resourcegraph.models import (
    QueryRequest,
    QueryRequestOptions,
    QueryResponse,
)
from router.user_details.user_details import (
    get_client_by_integration_name,
)
from router.untagged_resources.schemas import (
    ResourceTagConfig,
    Tag,
)


def list_azure_untagged_resources(subscription_id: str,integration_name:str):

    client_secrets = get_client_by_integration_name(integration_name)
    credential = ClientSecretCredential(
            tenant_id=client_secrets["tenant_id"],
            client_id=client_secrets["client_id"],
            client_secret=client_secrets["client_secret"],
        )
    client = ResourceGraphClient(credential)
    options = QueryRequestOptions(result_format="objectArray")

    query = QueryRequest(
        subscriptions=[subscription_id],
        query="resources | where isnull(tags) or tostring(tags) == '[]'",
        options=options,
    )

    results: QueryResponse = client.resources(query=query)
    return [
        ResourceTagConfig(
            resource_type=resource.get("type"),
            service=resource.get("type").split("/")[-1],
            region=resource.get("location"),
            resource_name_or_id=resource.get("id").split("/")[-1],
            resource_arn=resource.get("id"),
        )
        for resource in results.data
    ]


def tag_azure_resources(
    subscription_id: str,integration_name, resource_id: str, tags: list[Tag]
):

    client_secrets = get_client_by_integration_name(integration_name)

    credential = ClientSecretCredential(
            tenant_id=client_secrets["tenant_id"],
            client_id=client_secrets["client_id"],
            client_secret=client_secrets["client_secret"],
        )
    resource_client = ResourceManagementClient(credential, subscription_id)

    tags = {tag.key: tag.value for tag in tags}

    tag_patch_resource = TagsPatchResource(operation="Merge", properties={"tags": tags})

    resource_client.tags.begin_update_at_scope(resource_id, tag_patch_resource)

    return "tags applied"