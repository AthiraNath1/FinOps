import datetime as dt
import logging
import traceback
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterable, List

from azure.containerregistry import ContainerRegistryClient
from azure.core.exceptions import AzureError
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.containerregistry import ContainerRegistryManagementClient
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.network.models import VirtualNetworkGateway
from azure.mgmt.privatedns import PrivateDnsManagementClient
from azure.mgmt.recoveryservices import RecoveryServicesClient
from azure.mgmt.recoveryservicesbackup import RecoveryServicesBackupClient
from azure.mgmt.recoveryservicessiterecovery import SiteRecoveryManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import ResourceGroup
from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.web import WebSiteManagementClient
from azure.monitor.query import MetricAggregationType, MetricsQueryClient
# from sqlmodel import Session
from router.user_details.user_details import (
    get_client_by_integration_name,
)
# from finx_engine.core_dependencies.database import get_db
from router.orphan_resources import orphaned_cost_matrix as orphan_costs
from router.orphan_resources.orphaned_cost_matrix import (
    fetch_cost_app_service_plan,
    fetch_cost_disks,
    fetch_cost_load_balancer,
    fetch_cost_public_ip,
    get_app_gateway_monthly_cost,
    get_app_service_monthly_cost,
    get_nat_gateway_monthly_cost,
    get_orphaned_cost_app_gateway,
    get_orphaned_cost_nat_gateway,
    get_orphaned_cost_private_dns,
    get_orphaned_cost_vnet_gateway,
    get_private_dns_monthly_cost,
    get_single_database_monthly_cost,
    get_single_sql_database_orphan_cost,
    get_vnet_gateway_monthly_cost,
)


if TYPE_CHECKING:
    from azure.mgmt.network.models import ApplicationGateway
    from azure.mgmt.recoveryservicesbackup.activestamp.models import JobResource
    from azure.mgmt.sql.models import Database

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class OrphanedResources:
    resource_type: str | None
    resource_name: str | None
    resource_id: str | None
    resource_group: str
    location: str | None
    cost: float = 0.0
    orphaned_cost: float | None = (
        None  # None means not calculate or can't be calculated
    )


def sync_list_resource_groups(resource_client):
    try:
        return list(resource_client.resource_groups.list())
    except Exception:
        logging.exception("this is error mode")


def get_orphan_resource_list(
    resource_client,
    compute_client,
    network_client,
    web_client,
    resource_graph_client,
    private_dns_client,
    monitor_client,
    metrics_query_client,
    sql_client,
    client_credentials,
    subscription_id,
):
    try:
        orphaned_resource_list = []
        resource_groups = sync_list_resource_groups(
            resource_client,
        )
        # Use ThreadPool to process resource groups in parallel.
        with ThreadPoolExecutor() as executor:
            results = list(
                executor.map(
                    lambda rg: process_rg(
                        rg,
                        resource_client,
                        compute_client,
                        network_client,
                        web_client,
                        resource_graph_client,
                        private_dns_client,
                        monitor_client,
                        metrics_query_client,
                        sql_client,
                        client_credentials,
                        subscription_id,
                    ),
                    resource_groups,
                ),
            )

        for res in results:
            orphaned_resource_list.extend(res)

    except Exception:
        logging.exception("this is error mode")
    else:
        return orphaned_resource_list


def fetch_orphan_disks(rg, compute_client):
    try:
        resources = []
        for disk in compute_client.disks.list_by_resource_group(rg.name):
            if disk.disk_state == "Unattached":
                monthly_cost_disk = fetch_cost_disks(
                    disk.sku.name,
                    disk.disk_size_gb,
                    disk.disk_iops_read_write,
                    disk.disk_m_bps_read_write,
                )
                resources.append(
                    OrphanedResources(
                        disk.type,
                        disk.name,
                        disk.id,
                        rg.name,
                        disk.location,
                        monthly_cost_disk,
                    ),
                )

    except Exception:
        logging.exception("this is error mode")
    else:
        return resources


def fetch_orphan_av_sets(rg, compute_client):
    try:
        resources = []
        for av_set in compute_client.availability_sets.list(rg.name):
            if not av_set.virtual_machines:
                resources.append(
                    OrphanedResources(
                        av_set.type,
                        av_set.name,
                        av_set.id,
                        rg.name,
                        av_set.location,
                    ),
                )

    except Exception:
        logging.exception("this is error mode")
    else:
        return resources


def fetch_orphan_nsgs(rg, network_client):
    try:
        resources = []
        for nsg in network_client.network_security_groups.list(rg.name):
            if not (nsg.network_interfaces and nsg.subnets):
                resources.append(
                    OrphanedResources(
                        nsg.type,
                        nsg.name,
                        nsg.id,
                        rg.name,
                        nsg.location,
                    ),
                )
    except Exception:
        logging.exception("this is error mode")
    else:
        return resources


def fetch_orphan_public_ips(rg, network_client):
    try:
        resources = []
        for public_ip in network_client.public_ip_addresses.list(rg.name):
            if not (
                public_ip.ip_configuration
                or public_ip.nat_gateway
                or public_ip.public_ip_prefix
            ):
                monthly_cost_public_ip = fetch_cost_public_ip(
                    public_ip.public_ip_address_version,
                    public_ip.sku.name,
                    public_ip.sku.tier,
                    public_ip.public_ip_allocation_method,
                )
                resources.append(
                    OrphanedResources(
                        public_ip.type,
                        public_ip.name,
                        public_ip.id,
                        rg.name,
                        public_ip.location,
                        monthly_cost_public_ip,
                    ),
                )

    except Exception:
        logging.exception("this is error mode")
    else:
        return resources


def fetch_orphan_nics(rg, network_client):
    try:
        resources = []
        for nic in network_client.network_interfaces.list(rg.name):
            if not (
                nic.private_endpoint
                or nic.private_link_service
                or nic.hosted_workloads
                or nic.virtual_machine
            ):
                resources.append(
                    OrphanedResources(
                        nic.type,
                        nic.name,
                        nic.id,
                        rg.name,
                        nic.location,
                    ),
                )
    except Exception:
        logging.exception("this is error mode")
    else:
        return resources


def fetch_orphan_load_balancers(rg, network_client):
    try:
        resources = []
        for lb in network_client.load_balancers.list(rg.name):
            if not lb.backend_address_pools:
                monthly_cost_lb = fetch_cost_load_balancer(
                    lb.sku.name,
                    lb.load_balancing_rules,
                )
                resources.append(
                    OrphanedResources(
                        lb.type,
                        lb.name,
                        lb.id,
                        rg.name,
                        lb.location,
                        monthly_cost_lb,
                    ),
                )

    except Exception:
        logging.exception("this is error mode")
    else:
        return resources


def fetch_orphan_route_tables(rg, network_client):
    try:
        resources = []
        for rt in network_client.route_tables.list(rg.name):
            if not rt.subnets:
                resources.append(
                    OrphanedResources(rt.type, rt.name, rt.id, rg.name, rt.location),
                )
    except Exception:
        logging.exception("this is error mode")

    else:
        return resources


def fetch_orphan_app_service_plans(rg, web_client):
    try:
        resources = []
        for asp in web_client.app_service_plans.list_by_resource_group(rg.name):
            if asp.number_of_sites == 0:
                monthly_cost_asp = fetch_cost_app_service_plan(
                    asp.kind,
                    asp.sku.name,
                )
                resources.append(
                    OrphanedResources(
                        asp.type,
                        asp.name,
                        asp.id,
                        rg.name,
                        asp.location,
                        monthly_cost_asp,
                    ),
                )
    except Exception:
        logging.exception("this is error mode")
    else:
        return resources


def fetch_orphan_app_gateways(
    rg: ResourceGroup,
    network_client: NetworkManagementClient,
    resource_graph_client: ResourceGraphClient,
) -> list[OrphanedResources]:
    orphan_app_gateways: list[OrphanedResources] = []
    rg_name: str = rg.name  # type: ignore  # noqa: PGH003
    logger.info("Checking App Gateways for resource group %s", rg_name)
    try:
        app_gateways: Iterable[ApplicationGateway] = (
            network_client.application_gateways.list(resource_group_name=rg_name)
        )
    except AzureError as exc:
        message = f"Error fetching orphan application gateways in resource group {rg_name}: {exc!r}"
        logging.exception(message)

    for app_gateway in app_gateways:
        logging.info(
            "For application gateway %s in resource group %s, checking if it has any backend pools",
            app_gateway.name,
            rg_name,
        )
        backend_address_pools = app_gateway.backend_address_pools
        if backend_address_pools:
            backend_pool_names = [pool.name for pool in backend_address_pools]
            logger.info("Backend address pools: %s", backend_pool_names)
            all_ips = []
            for pool in backend_address_pools:
                addresses = pool.backend_addresses
                if addresses:
                    all_ips.extend([address.ip_address for address in addresses])
            logger.info("All backend IPs: %s", all_ips)
            if len(all_ips) > 0:
                logger.info(
                    "Application Gateway %s has backend IPs, skipping", app_gateway.name
                )
                continue

        orphan_app_gateways.append(
            OrphanedResources(
                resource_type=app_gateway.type,
                resource_name=app_gateway.name,
                resource_id=app_gateway.id,
                resource_group=rg_name,
                location=app_gateway.location,
                cost=get_app_gateway_monthly_cost(app_gateway),
                orphaned_cost=get_orphaned_cost_app_gateway(
                    app_gateway, resource_graph_client
                ),
            )
        )
    logger.info(
        "All orphaned application gateways in resource group %s: %s",
        rg_name,
        orphan_app_gateways,
    )
    return orphan_app_gateways


def fetch_orphan_vnet_gateways(
    rg: ResourceGroup, network_client: NetworkManagementClient
) -> list[OrphanedResources]:
    """Fetch orphaned VNet gateways in a resource group.

    Args:
    ----
        rg (ResourceGroup): Resource Group object for the resource group.
        network_client (NetworkManagementClient): Network Management Client object.

    Returns:
    -------
        list[OrphanedResources]: List of orphaned VNet gateways in the resource group.

    """

    def create_orphan_resource_from_vnet_gateway(
        vnet_gateway: VirtualNetworkGateway,
    ) -> OrphanedResources:
        return OrphanedResources(
            resource_type=vnet_gateway.type,
            resource_name=vnet_gateway.name,
            resource_id=vnet_gateway.id,
            resource_group=rg_name,
            location=vnet_gateway.location,
            cost=get_vnet_gateway_monthly_cost(vnet_gateway),
            orphaned_cost=get_orphaned_cost_vnet_gateway(vnet_gateway),
        )

    rg_name: str = rg.name  # type: ignore  # noqa: PGH003
    logger.info("Checking VNet Gateways for resource group %s", rg_name)
    try:
        vnet_gateways = list(network_client.virtual_network_gateways.list(rg_name))
    except AzureError as exc:
        message = (
            f"Error fetching orphan VNet gateways in resource group {rg_name}: {exc!r}"
        )
        logging.exception(message)

    if not vnet_gateways:
        logger.info("No orphan VNet gateways found in resource group %s", rg_name)
        return []

    connections = list(network_client.virtual_network_gateway_connections.list(rg_name))
    if not connections:
        logger.info("No VNet gateway connections found in resource group %s", rg_name)
        logger.debug(
            "All VNet gateways in resource group %s are not connected.", rg_name
        )
        return [
            create_orphan_resource_from_vnet_gateway(vnet_gateway)
            for vnet_gateway in vnet_gateways
        ]

    connected_vnet_gateway_ids = []
    for connection in connections:
        connected_vnet_gateway_ids.append(connection.virtual_network_gateway1.id)
        gateway2 = connection.virtual_network_gateway2
        if gateway2:
            connected_vnet_gateway_ids.append(gateway2.id)
    # removing repeated ids
    connected_vnet_gateway_ids = list(set(connected_vnet_gateway_ids))
    logger.info("Connected VNet Gateway IDs obtained.")
    logger.debug("Connected VNet Gateway IDs: %s", connected_vnet_gateway_ids)
    return [
        create_orphan_resource_from_vnet_gateway(vnet_gateway)
        for vnet_gateway in vnet_gateways
        if vnet_gateway.id not in connected_vnet_gateway_ids
    ]


def fetch_orphan_nat_gateways(
    rg: ResourceGroup, network_client: NetworkManagementClient
) -> list[OrphanedResources]:
    """Fetch orphaned NAT gateways in a resource group. NAT gateways that have no subnet and
    a public ip are considered orphaned.

    Args:
    ----
        rg (ResourceGroup): Resource Group object for the resource group.
        network_client (NetworkManagementClient): Network Management Client object.

    Returns:
    -------
        list[OrphanedResources]: List of orphaned NAT gateways in the resource group.

    """
    rg_name: str = rg.name  # type: ignore  # noqa: PGH003
    logger.info("Checking NAT Gateways for resource group %s", rg_name)
    try:
        nat_gateways = list(network_client.nat_gateways.list(rg_name))
    except AzureError as exc:
        message = (
            f"Error fetching orphan NAT gateways in resource group {rg_name}: {exc!r}"
        )
        logging.exception(message)

    if not nat_gateways:
        logger.info("No NAT gateways found in resource group %s", rg_name)
        return []

    orphan_resources: list[OrphanedResources] = []

    for nat_gateway in nat_gateways:
        if nat_gateway.subnets and nat_gateway.public_ip_addresses:
            logger.info(
                "NAT Gateway %s in resource group %s has subnets and public ips, skipping",
                nat_gateway.name,
                rg_name,
            )
            continue

        doesnt_have = ""
        if not nat_gateway.subnets and not nat_gateway.public_ip_addresses:
            doesnt_have += "subnets and public IPs"
        elif not nat_gateway.subnets:
            doesnt_have += "subnets"
        else:
            doesnt_have += "public IPs"
        logger.info("NAT Gateway %s doesn't have %s.", nat_gateway.name, doesnt_have)
        logger.info("Adding NAT Gateway %s to orphaned resources", nat_gateway.name)

        orphan_resources.append(
            OrphanedResources(
                resource_type=nat_gateway.type,
                resource_name=nat_gateway.name,
                resource_id=nat_gateway.id,
                resource_group=rg_name,
                location=nat_gateway.location,
                cost=get_nat_gateway_monthly_cost(nat_gateway),
                orphaned_cost=get_orphaned_cost_nat_gateway(nat_gateway),
            )
        )

    return orphan_resources


def fetch_orphan_private_dns_zones(
    rg: ResourceGroup,
    dns_client: PrivateDnsManagementClient,
    monitor_client: MonitorManagementClient,
) -> list[OrphanedResources]:
    """Fetch orphaned Private DNS zones in a resource group. Private DNS zones that have no virtual
    networks linked to them are considered orphaned.

    Args:
    ----
        rg (ResourceGroup): Resource Group object for the resource group.
        network_client (NetworkManagementClient): Network Management Client object.

    Returns:
    -------
        list[OrphanedResources]: List of orphaned Private DNS zones in the resource group.

    """
    rg_name: str = rg.name  # type: ignore  # noqa: PGH003
    logger.info("Checking Private DNS Zones for resource group %s", rg_name)
    try:
        private_dns_zones = list(
            dns_client.private_zones.list_by_resource_group(rg_name)
        )
    except AzureError as exc:
        message = f"Error fetching orphan Private DNS zones in resource group {rg_name}: {exc!r}"
        logging.exception(message)

    if not private_dns_zones:
        logger.info("No Private DNS zones found in resource group %s", rg_name)
        return []

    orphan_private_dns_zones: list[OrphanedResources] = []
    for private_dns_zone in private_dns_zones:
        logger.info(
            "Checking Private DNS Zone %s in resource group %s",
            private_dns_zone.name,
            rg_name,
        )
        number_of_linked_vnet: int = int(private_dns_zone.number_of_virtual_network_links)  # type: ignore  # noqa: PGH003
        logger.info(
            "Number of linked virtual networks connected to private dns %s: %s",
            private_dns_zone.name,
            number_of_linked_vnet,
        )
        if number_of_linked_vnet > 0:
            logger.info(
                "Private DNS Zone %s has linked virtual networks, skipping",
                private_dns_zone.name,
            )
            continue

        logger.info(
            "Adding Private DNS Zone %s to orphaned resources", private_dns_zone.name
        )
        orphan_private_dns_zones.append(
            OrphanedResources(
                resource_type=private_dns_zone.type,
                resource_name=private_dns_zone.name,
                resource_id=private_dns_zone.id,
                resource_group=rg_name,
                location=private_dns_zone.location,
                cost=get_private_dns_monthly_cost(private_dns_zone),
                orphaned_cost=get_orphaned_cost_private_dns(
                    private_dns_zone, monitor_client
                ),
            )
        )

    return orphan_private_dns_zones


def fetch_orphan_app_service_with_no_request(
    rg: ResourceGroup,
    web_client: WebSiteManagementClient,
    monitor_client: MonitorManagementClient,
    metrics_query_client: MetricsQueryClient,
) -> list[OrphanedResources]:
    """Fetch orphaned App Services in a resource group. App Services that have no requests in last
    30 days are considered orphaned.

    Args:
    ----
        rg (ResourceGroup): Resource Group object for the resource group.
        network_client (NetworkManagementClient): Network Management Client object.

    Returns:
    -------
        list[OrphanedResources]: List of orphaned App Services in the resource group.

    """
    rg_name: str = rg.name  # type: ignore  # noqa: PGH003
    logger.info("Checking App Services for resource group %s", rg_name)
    try:
        app_services = list(web_client.web_apps.list_by_resource_group(rg_name))
    except AzureError as exc:
        message = (
            f"Error fetching orphan App Services in resource group {rg_name}: {exc!r}"
        )
        logging.exception(message)

    if not app_services:
        logger.info("No App Services found in resource group %s", rg_name)
        return []

    def get_requests_in_last_30_days(app_service_id: str) -> int:
        try:
            result = metrics_query_client.query_resource(
                resource_uri=app_service_id,
                metric_names=["Requests"],
                timespan=dt.timedelta(days=30),
                aggregations=[MetricAggregationType.COUNT],
            )
            data = result.metrics[0].timeseries[0].data  # type: ignore  # noqa: PGH003
        except AzureError as exc:
            message = f"Error fetching request count for App Service {app_service_id}: {exc!r}"
            logging.exception(message)
        except KeyError as exc:
            message = (
                f"Error fetching requests for App Service {app_service_id}: {exc!r}"
            )
            logging.exception(message)
        else:
            return sum([point.count for point in data if point.count is not None])  # type: ignore  # noqa: PGH003
        return 0

    orphan_app_services: list[OrphanedResources] = []
    for app_service in app_services:
        logger.info(
            "Checking App Service %s in resource group %s", app_service.name, rg_name
        )
        app_service_id: str = app_service.id  # type: ignore  # noqa: PGH003
        request_count = get_requests_in_last_30_days(app_service_id)
        logger.info(
            "Request count for App Service %s in resource group %s: %s",
            app_service.name,
            rg_name,
            request_count,
        )
        if request_count > 0:
            logger.info(
                "App Service %s has requests in last 30 days, skipping",
                app_service.name,
            )
            continue

        logger.info("Adding App Service %s to orphaned resources", app_service.name)
        orphan_app_services.append(
            OrphanedResources(
                resource_type=app_service.type,
                resource_name=app_service.name,
                resource_id=app_service.id,
                resource_group=rg_name,
                location=app_service.location,
                cost=get_app_service_monthly_cost(app_service),  # type: ignore  # noqa: PGH003
            )
        )
    return orphan_app_services


def fetch_orphan_sql_databases(  # noqa: C901
    rg: ResourceGroup,
    sql_client: SqlManagementClient,
    monitor_client: MonitorManagementClient,
    metrics_query_client: MetricsQueryClient,
) -> list[OrphanedResources]:
    """Fetch orphaned SQL databases in a resource group. SQL databases that have no requests in last
    30 days are considered orphaned.

    Args:
    ----
        rg (ResourceGroup): Resource Group object for the resource group.
        sql_client (SqlManagementClient): SQL Management Client object.
        monitor_client (MonitorManagementClient): Monitor Management Client object.
        metrics_query_client (MetricsQueryClient): Metrics Query Client object.

    Returns:
    -------
        list[OrphanedResources]: List of orphaned SQL databases in the resource group.

    """
    rg_name: str = rg.name  # type: ignore  # noqa: PGH003
    logger.info("Checking SQL Databases for resource group %s", rg_name)
    try:
        servers = sql_client.servers.list_by_resource_group(rg_name)
    except AzureError as exc:
        message = (
            f"Error fetching orphan SQL Databases in resource group {rg_name}: {exc!r}"
        )
        logging.exception(message)

    if not servers:
        logger.info("No SQL Servers found in resource group %s", rg_name)
        return []

    databases: list[Database] = []
    for server in servers:
        server_name: str = server.name  # type: ignore  # noqa: PGH003
        try:
            database_by_server = sql_client.databases.list_by_server(
                rg_name, server_name
            )
            databases.extend(database_by_server)  # type: ignore  # noqa: PGH003
        except AzureError as exc:
            message = (
                f"Error fetching orphan SQL Databases in server {server_name}: {exc!r}"
            )
            logging.exception(message)

    def get_requests_in_last_30_days(database_id: str) -> int:
        try:
            result = metrics_query_client.query_resource(
                resource_uri=database_id,
                metric_names=["connection_successful"],
                timespan=dt.timedelta(days=30),
                aggregations=[MetricAggregationType.TOTAL],
            )
            data = result.metrics[0].timeseries[0].data  # type: ignore  # noqa: PGH003
        except AzureError as exc:
            message = (
                f"Error fetching request count for SQL Database {database_id}: {exc!r}"
            )
            logging.exception(message)
        except KeyError as exc:
            message = f"Error fetching requests for App Service {database_id}: {exc!r}"
            logging.exception(message)
        else:
            return sum([point.total for point in data if point.total is not None])  # type: ignore  # noqa: PGH003
        return 0

    orphan_sql_databases: list[OrphanedResources] = []
    for database in databases:
        logger.info(
            "Checking SQL Database %s in resource group %s", database.name, rg_name
        )
        id = database.id
        if id is None:
            logger.info("SQL Database %s doesn't have an ID, skipping", database.name)
            continue
        request_count = get_requests_in_last_30_days(id)

        if request_count > 0:
            logger.info(
                "SQL Database %s has requests in last 30 days, skipping",
                database.name,
            )
            continue

        logger.info("Adding SQL Database %s to orphaned resources", database.name)
        orphan_sql_databases.append(
            OrphanedResources(
                resource_type=database.type,
                resource_name=database.name,
                resource_id=id,
                resource_group=rg_name,
                location=database.location,
                cost=(
                    get_single_database_monthly_cost(database)
                    if database.current_sku.capacity > 0  # type: ignore  # noqa: PGH003
                    else 0
                ),
                orphaned_cost=(
                    get_single_sql_database_orphan_cost(database, monitor_client)
                    if database.current_sku.capacity > 0  # type: ignore  # noqa: PGH003
                    else None
                ),
            )
        )
    logger.info(
        "All orphaned SQL databases in resource group %s: %s",
        rg_name,
        orphan_sql_databases,
    )
    return orphan_sql_databases


def fetch_orphan_container_registry_repo_and_images(
    rg: ResourceGroup, client_credentials: ClientSecretCredential, subscription_id: str
) -> list[OrphanedResources]:
    """Fetch orphaned Container Registries, Repositories inside registries, and images inside
    repositories in a resource group. Registries are considered orphan if they have no images,
    repositories and images are considered orphan if there have been no modification (new image,
    update image version) in the last 30 days.

    Args:
    ----
        rg (ResourceGroup): Resource Group object for the resource group.
        client_credentials (ClientSecretCredential): Client Secret Credential object.
        subscription_id (str): Azure subscription ID.

    Returns:
    -------
        list[OrphanedResources]: List of orphaned Container Registries, Repositories, and Images in
        the resource group.

    """
    rg_name: str = rg.name  # type: ignore  # noqa: PGH003
    logger.info("Checking Container Registries for resource group %s", rg_name)
    try:
        container_management_client = ContainerRegistryManagementClient(
            client_credentials, subscription_id
        )
        registries = list(container_management_client.registries.list_by_resource_group(rg_name))  # type: ignore  # noqa: PGH003
    except AzureError as exc:
        message = f"Error fetching orphan Container Registries in resource group {rg_name}: {exc!r}"
        logger.exception(message)

    orphaned_registries: list[OrphanedResources] = []
    orphaned_repositories: list[OrphanedResources] = []
    orphaned_images: list[OrphanedResources] = []

    monitor_client = MonitorManagementClient(client_credentials, subscription_id)

    for registry in registries:
        try:
            registry_endpoint = f"https://{registry.login_server}"
            registry_client = ContainerRegistryClient(
                registry_endpoint, client_credentials
            )
            repository_names = registry_client.list_repository_names()
            image_count = 0
            for repository_name in repository_names:
                # Check if the repository has been modified in the last 30 days
                repository_properties = registry_client.get_repository_properties(
                    repository_name
                )
                last_modified = repository_properties.last_updated_on
                if check_date(last_modified, 30):
                    # Add repository to orphaned repositories
                    logger.info("Repository %s has been orphaned", repository_name)
                    orphaned_repositories.append(
                        OrphanedResources(
                            resource_type=f"{registry.type}/repositories",
                            resource_name=f"{registry.name}/{repository_name}",
                            resource_id=f"{registry.id}/repositories/{repository_name}",
                            resource_group=rg_name,
                            location=registry.location,
                        )
                    )
                images = registry_client.list_tag_properties(repository_name)
                for image in images:
                    # Check if the image has been modified in the last 30 days
                    image_count += 1
                    last_modified = image.last_updated_on
                    if check_date(last_modified, 30):
                        # Add image to orphaned images
                        logger.info("Image %s has been orphaned", image.name)
                        orphaned_images.append(
                            OrphanedResources(
                                resource_type=f"{registry.type}/repositories/images",
                                resource_name=f"{registry.name}/{repository_name}/{image.name}",
                                resource_id=(
                                    f"{registry.id}/repositories/{repository_name}"
                                    f"/images/{image.name}/{image.digest}"
                                ),
                                resource_group=rg_name,
                                location=registry.location,
                            )
                        )
                if image_count > 0:
                    # If images are found, skip the registry
                    logger.info(
                        "Container Registry %s has images, skipping", registry.name
                    )
                    continue
                # Add registry to orphaned registries
                logger.info("No images found in Container Registry %s", registry.name)
                orphaned_registries.append(
                    OrphanedResources(
                        resource_type=registry.type,
                        resource_name=registry.name,
                        resource_id=registry.id,
                        resource_group=rg_name,
                        location=registry.location,
                        cost=orphan_costs.get_container_registry_monthly_cost(registry),  # type: ignore  # noqa: PGH003
                        orphaned_cost=orphan_costs.get_container_registry_orphaned_cost(
                            registry, monitor_client  # type: ignore  # noqa: PGH003
                        ),
                    )
                )
        except AzureError as exc:
            logger.warning(
                "Error creating registry client for %s: %s", registry.name, exc
            )
            continue
        finally:
            registry_client.close()
    # Close the clients
    container_management_client.close()
    monitor_client.close()
    logger.info(
        "Orphaned registries, repositories and images in resource group %s obtained",
        rg_name,
    )
    logger.debug("Orphaned registries: %s", orphaned_registries)
    logger.debug("Orphaned repositories: %s", orphaned_repositories)
    logger.debug("Orphaned images: %s", orphaned_images)
    return orphaned_registries + orphaned_repositories + orphaned_images


def fetch_orphan_recovery_vaults(
    rg: ResourceGroup, client: ClientSecretCredential, subscription_id: str
) -> list[OrphanedResources]:
    """Fetch orphaned Recovery Vaults in a resource group. Recovery Vaults that have no backup
    items, replicated items or no backup job run in last 60 days are considered orphaned.

    Args:
    ----
        rg (ResourceGroup): Resource Group object for the resource group.
        client (ClientSecretCredential): Client Secret Credential object.
        subscription_id (str): Azure subscription ID.

    Returns:
    -------
        list[OrphanedResources]: List of orphaned Recovery Vaults in the resource group.

    """
    rg_name: str = rg.name  # type: ignore  # noqa: PGH003

    try:
        recovery_vault_client = RecoveryServicesClient(client, subscription_id)
        recovery_vaults = list(
            recovery_vault_client.vaults.list_by_resource_group(rg_name)
        )
    except AzureError as exc:
        message = f"Error fetching orphan Recovery Vaults in resource group {rg_name}: {exc!r}"
        logger.exception(message)

    orphaned_recovery_vaults: list[OrphanedResources] = []
    for recovery_vault in recovery_vaults:
        vault_name: str = recovery_vault.name  # type: ignore  # noqa: PGH003
        logger.info(
            "Checking Recovery Vault %s in resource group %s", vault_name, rg_name
        )
        try:
            recovery_backup_client = RecoveryServicesBackupClient(
                client, subscription_id
            )
            site_recovery_client = SiteRecoveryManagementClient(
                client, subscription_id, rg_name, vault_name
            )

            backup_items = recovery_backup_client.backup_protected_items.list(
                vault_name, rg_name
            )
            replicated_items = site_recovery_client.replication_protected_items.list()
            backup_items_count = sum(1 for _ in backup_items)
            logger.info(
                "There are %s backup items in vault %s", backup_items_count, vault_name
            )
            replicated_items_count = sum(1 for _ in replicated_items)
            logger.info(
                "There are %s replicated items in vault %s",
                replicated_items_count,
                vault_name,
            )
            total_items = backup_items_count + replicated_items_count

            latest_backup_time: dt.datetime | None = None
            backup_jobs = recovery_backup_client.backup_jobs.list(vault_name, rg_name)
            # Backup Jobs are sorted, latest job is the first one
            latest_backup_job: JobResource = next(backup_jobs, None)  # type: ignore  # noqa: PGH003
            if latest_backup_job:
                job = latest_backup_job.properties
                if job:
                    latest_backup_time = job.start_time
            logger.info("Latest backup job time: %s", latest_backup_time)

            # If there are no items or no backup job run in last 60 days, add to orphaned resources
            if (
                total_items == 0
                or not latest_backup_time
                or check_date(latest_backup_time, 60)
            ):
                logger.info(
                    "Adding Recovery Vault %s to orphaned resources", vault_name
                )
                orphaned_recovery_vaults.append(
                    OrphanedResources(
                        resource_type=recovery_vault.type,
                        resource_name=vault_name,
                        resource_id=recovery_vault.id,
                        resource_group=rg_name,
                        location=recovery_vault.location,
                    )
                )

        except AzureError as exc:
            logger.warning("Error fetching details of vault %s: %s", vault_name, exc)
            continue
        finally:
            recovery_backup_client.close()
            site_recovery_client.close()

    recovery_vault_client.close()
    return orphaned_recovery_vaults


def process_rg(
    rg,
    resource_client,
    compute_client,
    network_client,
    web_client,
    resource_graph_client,
    private_dns_client,
    monitor_client,
    metrics_query_client,
    sql_client,
    client_credentials,
    subscription_id,
):
    try:
        tasks = [
            fetch_orphan_disks(rg, compute_client),
            fetch_orphan_av_sets(rg, compute_client),
            fetch_orphan_nsgs(rg, network_client),
            fetch_orphan_public_ips(rg, network_client),
            fetch_orphan_nics(rg, network_client),
            fetch_orphan_load_balancers(rg, network_client),
            fetch_orphan_route_tables(rg, network_client),
            fetch_orphan_app_service_plans(rg, web_client),
            fetch_orphan_app_gateways(rg, network_client, resource_graph_client),
            fetch_orphan_vnet_gateways(rg, network_client),
            fetch_orphan_nat_gateways(rg, network_client),
            fetch_orphan_private_dns_zones(rg, private_dns_client, monitor_client),
            fetch_orphan_app_service_with_no_request(
                rg, web_client, monitor_client, metrics_query_client
            ),
            fetch_orphan_sql_databases(
                rg, sql_client, monitor_client, metrics_query_client
            ),
            fetch_orphan_container_registry_repo_and_images(
                rg, client_credentials, subscription_id
            ),
        ]

    except Exception:
        logging.exception("this is error mode")
    else:
        return [item for sublist in tasks for item in sublist]


def generate_orphan_resources(
   integration_name:str,
   subscription_id: str,
) -> list[OrphanedResources]:
    try:
        # secrets = get_client_by_integration_name(integration_name)
        client_secrets = get_client_by_integration_name(integration_name)
        credential = ClientSecretCredential(
            tenant_id=client_secrets["tenant_id"],
            client_id=client_secrets["client_id"],
            client_secret=client_secrets["client_secret"],
        )
        # credential = ClientSecretCredential(
        #       tenant_id = '5b956597-aaf0-45b1-aa8c-78023da8463c',
        # client_id = '80b15c47-2b6d-4576-a7e9-6d7372a58eb9',
        # client_secret = 'nng8Q~UxQ7A_vRir5ipJJcIhjgohOSk7R6UhLcVT'
        # )
        resource_client = ResourceManagementClient(credential, subscription_id)
        compute_client = ComputeManagementClient(credential, subscription_id)
        network_client = NetworkManagementClient(credential, subscription_id)
        web_client = WebSiteManagementClient(credential, subscription_id)
        resource_graph_client = ResourceGraphClient(credential)
        private_dns_client = PrivateDnsManagementClient(credential, subscription_id)
        monitor_management_client = MonitorManagementClient(credential, subscription_id)
        metrics_query_client = MetricsQueryClient(credential)
        sql_client = SqlManagementClient(credential, subscription_id)
        orphan_resources = get_orphan_resource_list(
            resource_client,
            compute_client,
            network_client,
            web_client,
            resource_graph_client,
            private_dns_client,
            monitor_management_client,
            metrics_query_client,
            sql_client,
            credential,
            subscription_id,
        )
    except Exception:
        logging.exception("this is error mode")
        return []
    else:
        return orphan_resources  # type: ignore  # noqa: PGH003


def delete_resources_by_ids(
    resource_ids: List[str],
    integration_name: str,
    subscription_id: str,
    
) -> dict:
    try:
        """
        Delete resources based on a list of resource IDs.

        :param resource_id: List of resource IDs.
        :param subscription_id: Azure subscription ID.
        :return: Status message.
        """

        # secrets = get_client_by_integration_name(integration_name)
        client_secrets = get_client_by_integration_name(integration_name)
        credential = ClientSecretCredential(
            tenant_id=client_secrets["tenant_id"],
            client_id=client_secrets["client_id"],
            client_secret=client_secrets["client_secret"],
        )
        # credential = ClientSecretCredential(
        #       tenant_id = '5b956597-aaf0-45b1-aa8c-78023da8463c',
        # client_id = '80b15c47-2b6d-4576-a7e9-6d7372a58eb9',
        # client_secret = 'nng8Q~UxQ7A_vRir5ipJJcIhjgohOSk7R6UhLcVT'
        # )
        resource_client = ResourceManagementClient(credential, subscription_id)
        delete_operations = []
        with ThreadPoolExecutor() as executor:
            for resource_id in resource_ids:
                if (
                    ("publicIPAddresses" in resource_id)
                    or ("serverfarms" in resource_id)
                    or ("networkSecurityGroups" in resource_id)
                ):
                    api_version = "2022-09-01"
                elif "disks" in resource_id:
                    api_version = "2023-04-02"
                else:
                    api_version = "2022-04-01"  # Default API version
                try:
                    current_delete_operation = executor.submit(
                        resource_client.resources.begin_delete_by_id,
                        resource_id,
                        api_version,
                    )  # Update the API version
                    delete_operations.append(current_delete_operation)
                except Exception as e:
                    logging.exception("this is deletion error mode")
                    return {"status": "Error", "message": str(e)}
        for operation in delete_operations:
            try:
                operation.result()
            except Exception as e:
                logging.exception("this is operation error mode")
                return {
                    "status": "Error",
                    "message": str(e),
                    "details": traceback.format_exc(),
                }
    except Exception:
        logging.exception("this is error mode")
    else:
        return {"status": "Resource deleted successfully."}


def check_date(date: dt.datetime, days: int) -> bool:
    """Check if the date is older than the specified number of days.

    Args:
    ----
        date (dt.datetime): Date to check.
        days (int): Number of days.

    Returns:
    -------
        bool: True if the date is older than the specified number of days, False otherwise.

    """
    return dt.datetime.now(dt.UTC) - date > dt.timedelta(days=days)


if __name__ == "__main__":
    pass