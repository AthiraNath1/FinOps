from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.containerregistry import ContainerRegistryManagementClient
from azure.mgmt.databricks import AzureDatabricksManagementClient
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.eventhub import EventHubManagementClient
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.kusto import KustoManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.web import WebSiteManagementClient
from router.user_details.user_details import (
    get_client_by_integration_name,
)
# from sqlmodel import Session

# from finx_engine.core_dependencies.database import get_db
from router.networking.schemas import (
    NetworkBaseDetail,
    NetworkDetails,
    ResourceType,
)
# from finx_engine.services.user_details.user_details import (
#     get_client_by_integration_name,
# )


class NetworkManagement:
    def __init__(
        self, integration_name,subscription_id: str
    ):
        secrets = get_client_by_integration_name(integration_name)


        self.credential = ClientSecretCredential(
         tenant_id=secrets["tenant_id"],
            client_id=secrets["client_id"],
            client_secret=secrets["client_secret"],
        )
        self.subscription_id = str(subscription_id)

    def list_resource_by_subscription(self):
        # get the resource list of an sub_id

        resource_map = {
            "Microsoft.Compute/disks": ResourceType.disks,
            "Microsoft.ContainerRegistry/registries": ResourceType.registries,
            "Microsoft.Sql/servers": ResourceType.servers,
            "Microsoft.Web/sites": ResourceType.web_apps,
            "Microsoft.Databricks/workspaces": ResourceType.workspaces,
            "Microsoft.EventHub/namespaces": ResourceType.namespaces,
            "Microsoft.Kusto/clusters": ResourceType.clusters,
            "Microsoft.KeyVault/vaults": ResourceType.vaults,
            "Microsoft.DataFactory/factories": ResourceType.factories,
        }

        resource_client = ResourceManagementClient(
            self.credential, self.subscription_id
        )

        resource_list = (
            resource_client.resources.list()
        )  # command to get all resource in a subs

        result_resource_list: list[NetworkBaseDetail] = []
        for each_resource in resource_list:
            resource_group = each_resource.id.split("/")[4]  # get the rg name
            resource_type = resource_map.get(each_resource.type)
            if resource_type:
                result_resource_list.append(
                    NetworkBaseDetail(
                        resource_group_name=resource_group,
                        resource_type=resource_type.name,
                        resource_name=each_resource.name,
                    )
                )
        return result_resource_list

    def get_network(self):
        resource_type_to_client_mapping = {
            "disks": ComputeManagementClient,
            "registries": ContainerRegistryManagementClient,
            "servers": SqlManagementClient,
            "web_apps": WebSiteManagementClient,
            "workspaces": AzureDatabricksManagementClient,
            "namespaces": EventHubManagementClient,
            "clusters": KustoManagementClient,
            "vaults": KeyVaultManagementClient,
            "factories": DataFactoryManagementClient,
        }
        subscription_components = self.list_resource_by_subscription()
        network_details_list = []

        for component in subscription_components:
            resource_name = component.resource_name
            resource_group_name = component.resource_group_name
            resource_type_value = component.resource_type

            client_class = resource_type_to_client_mapping.get(resource_type_value)(
                self.credential, self.subscription_id
            )

            component_properties = getattr(client_class, resource_type_value, None)
            if component_properties:
                resource_specific_properties = component_properties.get(
                    resource_group_name, resource_name
                )

                is_public_network_access = None
                if resource_type_value.lower() == "vaults":
                    is_public_network_access = getattr(
                        resource_specific_properties.properties,
                        "public_network_access",
                        None,
                    )
                else:
                    is_public_network_access = getattr(
                        resource_specific_properties, "public_network_access", None
                    )

                resource_type_new = getattr(ResourceType, resource_type_value).value

                network_details_list.append(
                    NetworkDetails(
                        enabled_to_public=is_public_network_access,
                        subscription_id=self.subscription_id,
                        resource_group_name=resource_group_name,
                        resource_name=resource_name,
                        resource_type=resource_type_new,
                    )
                )

        return network_details_list