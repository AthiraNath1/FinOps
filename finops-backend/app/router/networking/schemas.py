from enum import Enum

from pydantic import BaseModel, validator


class ResourceType(Enum):
    disks = "Microsoft.Compute/disks"
    registries = "Microsoft.ContainerRegistry/registries"
    servers = "Microsoft.Sql/servers"
    web_apps = "Microsoft.Web/sites"
    workspaces = "Microsoft.Databricks/workspaces"
    namespaces = "Microsoft.EventHub/namespaces"
    clusters = "Microsoft.Kusto/clusters"
    vaults = "Microsoft.KeyVault/vaults"
    factories = "Microsoft.DataFactory/factories"


class NetworkBaseDetail(BaseModel):
    resource_group_name: str
    resource_type: str
    resource_name: str


class NetworkDetails(NetworkBaseDetail):
    subscription_id: str
    enabled_to_public: bool

    @validator("enabled_to_public", pre=True, check_fields=True)
    @classmethod
    def is_resource_public(cls, v):
        if isinstance(v, str) and v.lower() == "enabled":
            return True
        return False