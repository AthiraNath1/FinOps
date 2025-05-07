import logging
from datetime import UTC, datetime, timedelta

from azure.mgmt.containerregistry.models import Registry, SkuName
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.monitor.models import EventData
from azure.mgmt.network.models import (
    ApplicationGateway,
    ApplicationGatewaySkuName,
    NatGateway,
    VirtualNetworkGateway,
    VirtualNetworkGatewaySkuName,
)
from azure.mgmt.privatedns.models import PrivateZone
from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.resourcegraph.models import QueryRequest
from azure.mgmt.sql.models import Database, Sku
from azure.mgmt.web.models import Site

from router.orphan_resources import azure_pricing
from router.orphan_resources.azure_pricing import (
    APP_GATEWAY_PRICING,
    DTU_BASED_SQL_PRICING,
    NAT_GATEWAY_PRICING,
    PRIVATE_DNS_ZONE_PRICING,
    PROVISIONED_PRICING,
    SERVERLESS_PRICING,
    VNET_GATEWAY_PRICING,
)

logger = logging.getLogger(__name__)


HOURS_IN_MONTH = 24 * 30
# Define lookup tables
DISKS_COST_TABLES = {
    "StandardSSD_LRS": {
        4: 0.28,
        8: 0.56,
        16: 1.11,
        32: 2.21,
        64: 4.41,
        128: 8.81,
        256: 17.62,
        512: 35.23,
        1024: 70.46,
        2048: 140.92,
        4096: 281.83,
        8192: 563.65,
        16384: 1127.29,
        32767: 2254.58,
    },
    "Standard_LRS": {
        32: 1.41,
        64: 2.76,
        128: 5.41,
        256: 10.40,
        512: 19.97,
        1024: 37.58,
        2048: 75.16,
        4096: 150.31,
        8192: 300.62,
        16384: 601.23,
        32767: 1202.45,
    },
    "Premium_LRS": {
        4: 0.72,
        8: 1.44,
        16: 2.87,
        32: 5.33,
        64: 10.30,
        128: 19.89,
        256: 38.36,
        512: 73.89,
        1024: 136.40,
        2048: 261.40,
        4096: 500.07,
        8192: 954.68,
        16384: 1818.43,
        32767: 3636.85,
    },
}

PUBLIC_IP_COST_TABLE = {
    ("IPv4", "Standard", "Global"): 0.0091 * HOURS_IN_MONTH,
    ("IPv4", "Standard", "Regional"): 0.0046 * HOURS_IN_MONTH,
    ("IPv4", "Basic", "Dynamic"): 0.00364 * HOURS_IN_MONTH,
    ("IPv4", "Basic", "Static"): 0.00328 * HOURS_IN_MONTH,
}

LOAD_BALANCER_COST_TABLE = {
    ("Gateway",): 0.012 * HOURS_IN_MONTH,
    ("Standard",): 0.023 * HOURS_IN_MONTH,
    ("Standard", "additional"): 0.010 * HOURS_IN_MONTH,
}

APP_SERVICE_PLAN_COST_TABLE = {
    ("linux", "F1"): 0,
    ("linux", "B1"): 12.055,
    ("linux", "B2"): 24.109,
    ("linux", "B3"): 47.549,
    ("linux", "S1"): 63.621,
    ("linux", "S2"): 127.242,
    ("linux", "S3"): 254.484,
    ("linux", "P1v2"): 77.015,
    ("linux", "P2v2"): 154.700,
    ("linux", "P3v2"): 309.399,
    ("linux", "P0v3"): 77.685,
    ("linux", "P1v3"): 119.206,
    ("linux", "P1mv3"): 143.047,
    ("linux", "P2v3"): 238.412,
    ("linux", "P2mv3"): 286.094,
    ("linux", "P3v3"): 476.823,
    ("linux", "P3mv3"): 572.187,
    ("linux", "P4mv3"): 1144.374,
    ("linux", "P5mv3"): 2288.747,
    ("linux", "I1"): 190.863,
    ("linux", "I2"): 381.726,
    ("linux", "I3"): 763.452,
    ("linux", "I1v2"): 273.905,
    ("linux", "I2v2"): 547.810,
    ("linux", "I3v2"): 1095.620,
    ("linux", "I4v2"): 2191.239,
    ("linux", "I5v2"): 4382.478,
    ("linux", "I6v2"): 8764.956,
    ("windows", "F1"): 0,
    ("windows", "D1"): 8.707,
    ("windows", "B1"): 50.228,
    ("windows", "B2"): 100.455,
    ("windows", "B3"): 200.909,
    ("windows", "S1"): 66.970,
    ("windows", "S2"): 133.939,
    ("windows", "S3"): 267.878,
    ("windows", "P1v2"): 133.939,
    ("windows", "P2v2"): 267.878,
    ("windows", "P3v2"): 535.756,
    ("windows", "P0v3"): 143.985,
    ("windows", "P1v3"): 226.357,
    ("windows", "P1mv3"): 250.198,
    ("windows", "P2v3"): 452.714,
    ("windows", "P2mv3"): 500.396,
    ("windows", "P3v3"): 905.427,
    ("windows", "P3mv3"): 1000.791,
    ("windows", "P4mv3"): 2001.582,
    ("windows", "P5mv3"): 4003.164,
    ("windows", "I1"): 200.909,
    ("windows", "I2"): 401.817,
    ("windows", "I3"): 803.633,
    ("windows", "I1v2"): 381.726,
    ("windows", "I2v2"): 763.452,
    ("windows", "I3v2"): 1526.903,
    ("windows", "I4v2"): 3053.805,
    ("windows", "I5v2"): 6107.610,
    ("windows", "I6v2"): 12215.220,
}


def fetch_cost_disks(name, size, iops, mbps):
    try:
        if name == "PremiumV2_LRS":
            gib_cost = size * 0.088
            iops_cost = max(iops - 3000, 0) * 0.0054
            mbps_cost = max(mbps - 125, 0) * 0.044
            return gib_cost + iops_cost + mbps_cost

        return DISKS_COST_TABLES[name][size]
    except Exception:
        logging.exception("this is error mode")
        return 3.00


def fetch_cost_public_ip(version, name, tier, allocation):
    try:
        return PUBLIC_IP_COST_TABLE.get((version, name, tier), 0)
    except Exception:
        logging.exception("this is error mode")


def fetch_cost_load_balancer(name, rules):
    try:
        cost = LOAD_BALANCER_COST_TABLE[name][0]
        if "additional" in rules:
            cost += (len(rules) - 5) * LOAD_BALANCER_COST_TABLE[name][1]
    except Exception:
        logging.exception("this is error mode")
        return 0
    else:
        return cost


def fetch_cost_app_service_plan(kind, name):
    try:
        return APP_SERVICE_PLAN_COST_TABLE.get((kind, name), 0)
    except Exception:
        logging.exception("this is error mode")


def fetch_aws_cost_ebs(type: str, size: int, iops: int, throughput: int):
    ebs_cost = None
    if iops == None:
        iops = 0
    if throughput == None:
        throughput = 0
    if type == "gp2":
        ebs_cost = 0.119 * size
    elif type == "gp3":
        gp3_size_cost = 0.0952 * size
        gp3_iops_cost = 0
        gp3_throughput_cost = 0
        if iops > 3000:
            gp3_extra_iops = iops - 3000
            gp3_iops_cost = gp3_extra_iops * 0.006
        if throughput > 125:
            gp3_extra_throughput = throughput - 125
            gp3_throughput_cost = gp3_extra_throughput * 0.048
        ebs_cost = gp3_size_cost + gp3_iops_cost + gp3_throughput_cost
    elif type == "io2":
        io2_size_cost = 0.149 * size
        io2_iops_cost = 0
        if iops <= 32000:
            io2_iops_cost = 0.078 * iops
        if iops > 32000 and iops <= 64000:
            io2_iops_cost = (0.078 * 32000) + (0.055 * (iops - 32000))
        if iops > 64000:
            io2_iops_cost = (0.078 * 32000) + (0.055 * 32000) + (0.038 * (iops - 64000))
        ebs_cost = io2_size_cost + io2_iops_cost
    elif type == "io1":
        io1_size_cost = 0.149 * size
        io1_iops_cost = 0.078 * iops
        ebs_cost = io1_size_cost + io1_iops_cost
    elif type == "sc1":
        ebs_cost = 0.018 * size
    elif type == "st1":
        ebs_cost = 0.054 * size
    else:
        ebs_cost = 0
    return ebs_cost


def fetch_aws_eip_cost():
    cost_per_hour = 0.005

    hours_per_month = 24 * 30

    return cost_per_hour * hours_per_month


def aws_elb_cost(resource_type: str):
    if resource_type == "application load balancer":
        cost = 0.027 * 24 * 30
    elif resource_type == "gateway load balancer":
        cost = 0.0147 * 24 * 30
    elif resource_type == "network load balancer":
        cost = 0.027 * 24 * 30
    elif resource_type == "classic load balancer":
        cost = 0.03 * 24 * 30
    return cost


def aws_ami_cost(type: str, size: int, iops: int, throughput: int):

    snapshot_cost = 0.054 * size

    ebs_cost = fetch_aws_cost_ebs(type, size, iops, throughput)

    return snapshot_cost + ebs_cost


def get_app_gateway_monthly_cost(gateway: ApplicationGateway) -> float:
    """Get monthly expenditure for an application gateway.

    Args:
    ----
        gateway (ApplicationGateway): Application Gateway of Azure.

    Returns:
    -------
        float: Monthly cost of the application gateway.

    """
    basic_v1 = 0.0275  # Pricing per hour for Basic V2 app gateway
    sku_name: ApplicationGatewaySkuName = gateway.sku.name  # type: ignore  # noqa: PGH003
    logger.info(
        "Application Gateway with id: %s has sku name: %s", gateway.id, sku_name
    )
    app_gateway_pricing_per_hour = APP_GATEWAY_PRICING.get(sku_name, basic_v1)
    logger.info(
        "Pricing per hour for Application Gateway: %s", app_gateway_pricing_per_hour
    )
    return round(app_gateway_pricing_per_hour * HOURS_IN_MONTH, 2)


def get_orphaned_cost_app_gateway(
    gateway: ApplicationGateway, resource_graph_client: ResourceGraphClient
) -> float | None:
    """Get cost till now, which was unnecessary, if the resource was not orphaned.

    Args:
    ----
        gateway (ApplicationGateway): An Application Gateway object with app gateway details.
        resource_graph_client (_type_): Resource Graph client object.

    Returns:
    -------
        float | None: Cost of the Application Gateway till now from when it was orphaned.
        None if the orphaned_cost was not implemented.

    """
    query = f"""
    Resources
    | where type == 'microsoft.network/applicationgateways'
    | where id == '{gateway.id}'
    | project name, lastModifiedTime=properties.lastModifiedTime
    """
    request = QueryRequest(query=query)
    result = resource_graph_client.resources(request)
    logger.debug("Result of query: %s", result.data)
    last_modified_time = result.data[0]["lastModifiedTime"] if result.data else None  # type: ignore  # noqa: PGH003
    logger.info(
        "Last modified time for app gateway: %s is %s", gateway.name, last_modified_time
    )
    return None


def get_vnet_gateway_monthly_cost(vnet: VirtualNetworkGateway) -> float:
    """Get monthly expenditure for an virtual network gateway.

    Args:
    ----
        vnet (VirtualNetworkGateway): Virtual Network Gateway of Azure.

    Returns:
    -------
        float: Monthly cost of the virtual network gateway.

    """
    sku_name: VirtualNetworkGatewaySkuName = vnet.sku.name  # type: ignore  # noqa: PGH003
    logger.info(
        "Virtual Network Gateway with id: %s has sku name: %s", vnet.id, sku_name
    )
    vnet_gateway_price_per_hour = VNET_GATEWAY_PRICING.get(sku_name, 0.04)
    logger.info(
        "Pricing per hour for Virtual Network Gateway of sku %s: %s",
        sku_name,
        vnet_gateway_price_per_hour,
    )
    monthly_cost = vnet_gateway_price_per_hour * HOURS_IN_MONTH
    logger.info("Monthly cost for Virtual Network Gateway: %s", monthly_cost)
    return round(monthly_cost, 2)


def get_orphaned_cost_vnet_gateway(vnet: VirtualNetworkGateway) -> float | None:
    """Get estimated unnecessary expense done till now from when it was orphaned for a VNet Gateway.

    Args:
    ----
        vnet (VirtualNetworkGateway): Virtual Network Gateway object with details.

    Returns:
    -------
        float: Estimated unnecessary expense done till now from when it was orphaned.

    """
    etag = vnet.etag
    logger.info("Etag for VNet Gateway: %s is %s", vnet.name, etag)
    return None


def get_nat_gateway_monthly_cost(nat_gateway: NatGateway) -> float:
    """Get monthly expenditure for an NAT gateway.

    Args:
    ----
        nat_gateway (NatGateway): NAT Gateway of Azure.

    Returns:
    -------
        float: Monthly cost of the NAT gateway.

    """
    price_per_hour = NAT_GATEWAY_PRICING
    logger.info("Pricing per hour for NAT Gateway: %s", price_per_hour)
    price_per_month = price_per_hour * HOURS_IN_MONTH
    logger.info("Monthly cost for NAT Gateway: %s", price_per_month)
    return round(price_per_month, 2)


def get_orphaned_cost_nat_gateway(nat_gateway: NatGateway) -> float | None:
    """Get estimated unnecessary expense done till now from when it was orphaned for a NAT Gateway.

    Args:
    ----
        nat_gateway (NatGateway): NAT Gateway object with details.

    Returns:
    -------
        float | None: Estimated unnecessary expense done till now from when it was orphaned.

    """
    etag = nat_gateway.etag
    logger.info("Etag for NAT Gateway: %s is %s", nat_gateway.name, etag)
    # TODO: Implement this function (looking for ways)
    return None


def get_private_dns_monthly_cost(dns: PrivateZone) -> float:
    """Get monthly expenditure for a private DNS.

    Args:
    ----
        dns (PrivateZone): Private DNS of Azure.

    Returns:
    -------
        float: Monthly cost of the private DNS.

    """
    daily_cost = PRIVATE_DNS_ZONE_PRICING
    logger.info("Daily cost for Private DNS Zone: %s", daily_cost)
    monthly_cost = daily_cost * 30
    logger.info("Monthly cost for Private DNS Zone: %s", monthly_cost)
    return round(monthly_cost, 2)


def get_orphaned_cost_private_dns(
    dns: PrivateZone, monitor_client: MonitorManagementClient
) -> float:
    """Get estimated unnecessary expense done till now from when it was orphaned for a Private DNS.

    Args:
    ----
        dns (PrivateZone): Private DNS object with details.
        monitor_client (MonitorManagementClient): Monitor Management Client object.

    Returns:
    -------
        float: Estimated unnecessary expense done till now from when it was orphaned.

    """
    zone_name = dns.name
    logger.info("Zone name for Private DNS Zone: %s", zone_name)
    resource_id: str = dns.id  # type: ignore  # noqa: PGH003
    logger.info("Resource Id for Private DNS Zone: %s", resource_id)

    activity_logs = get_activity_log_with_resource_id(resource_id, monitor_client)
    # if there is no activity, that means there is no event in last 30 days so,
    if not activity_logs:
        # Resource has been orphaned for at least 90 days
        price_per_day = PRIVATE_DNS_ZONE_PRICING
        return round(price_per_day * 90, 2)

    # Sort the event timestamps so recent is the last item.
    event_times = sorted([event.event_timestamp for event in activity_logs])  # type: ignore  # noqa: PGH003
    logger.info("Event timestamps for the resource %s: %s", resource_id, event_times)

    most_recent_activity_at: datetime = event_times[-1]
    now = datetime.now(UTC)
    logger.info("Most recent activity at: %s", most_recent_activity_at)
    logger.info("Current time: %s", now)
    no_activity_for_days = (now - most_recent_activity_at).days + 1
    # 1 is added because resource minimum billing period is 1 day
    logger.info("No activity for days: %s", no_activity_for_days)

    orphaned_cost = PRIVATE_DNS_ZONE_PRICING * no_activity_for_days
    logger.info("Orphaned cost for Private DNS Zone %s: %s", zone_name, orphaned_cost)
    return round(orphaned_cost, 2)


def get_activity_log_with_resource_id(
    resource_id: str, monitor_client: MonitorManagementClient
) -> list[EventData]:
    """Get activity logs for a resource id for a resource in Azure for last 90 days.

    Args:
    ----
        resource_id (str): Resource Id of the azure resource
        monitor_client (MonitorManagementClient): Monitor Management Client object.

    Returns:
    -------
        list[EventData]: List of logs (EventData) for the resource id.

    """
    end_time = datetime.now(UTC)
    start_time = end_time - timedelta(days=90)
    logger.info("Start time: %s, End time: %s", start_time, end_time)

    filter_query = (
        f"eventTimestamp ge '{start_time.isoformat()}' and "
        f"eventTimestamp le '{end_time.isoformat()}' and "
        f"resourceUri eq '{resource_id}' "
    )
    return list(
        monitor_client.activity_logs.list(
            filter=filter_query,
            select="eventTimestamp,operationName,status",
        )
    )


def get_app_service_monthly_cost(app_service: Site) -> float:
    """Get monthly expenditure for an app service.

    Args:
    ----
        app_service (Site): App Service of Azure.

    Returns:
    -------
        float: Monthly cost of the app service.

    """
    return 0.0


def get_single_database_monthly_cost(database: Database) -> float:
    """Get monthly expenditure for a single database.

    Args:
    ----
        database (Database): Database of Azure.

    Returns:
    -------
        float: Monthly cost of the database.

    """
    sku: Sku = database.current_sku  # type: ignore  # noqa: PGH003
    logger.info("Sku for the database %s: %s", database.name, sku.name)
    capacity: int = sku.capacity  # type: ignore  # noqa: PGH003
    tier: str = sku.tier  # type: ignore  # noqa: PGH003
    family: str = sku.family  # type: ignore  # noqa: PGH003
    name: str = sku.name  # type: ignore  # noqa: PGH003
    logger.info(
        "Capacity: %s, Tier: %s, Family: %s, Name: %s, for database %s",
        capacity,
        tier,
        family,
        name,
        database.name,
    )
    kind: str = database.kind  # type: ignore  # noqa: PGH003
    logger.info("Kind of the database %s: %s", database.name, kind)
    type_of_database = kind.split(",")
    is_serverless: bool = "serverless" in type_of_database
    is_vcore: bool = "vcore" in type_of_database

    basic_price = DTU_BASED_SQL_PRICING.get(5, 0)

    price_per_hour: float = basic_price

    tier_mapping: dict[str, str] = {
        "GeneralPurpose": "GENERAL_PURPOSE",
        "BusinessCritical": "BUSINESS_CRITICAL",
        "Hyperscale": "HYPERSCALE",
    }
    tier = tier_mapping.get(tier, "GENERAL_PURPOSE")

    family = family.lower()
    if "fsv" in family:
        family = "FSV2"
    elif "gen" in family:
        family = "GEN5"
    elif family == "moprms":
        family = "PREMIUM_SERIES_MEMORY_OPTIMISED"
    elif family == "prms":
        family = "PREMIUM_SERIES"
    elif "dc" in family:
        family = "DC_SERIES"
    else:
        family = "GEN5"

    if not is_vcore:  # If the database is not vcore based i.e. DTU based
        price_per_hour = DTU_BASED_SQL_PRICING.get(capacity, basic_price)
    elif is_serverless:
        logger.info(
            "Price calculated using family %s and tier %s for serverless database %s",
            family,
            tier,
            database.name,
        )
        price_per_hour = (
            SERVERLESS_PRICING.get(family, {}).get(tier, basic_price) * capacity
        )
    else:
        logger.info(
            "Price calculated using family %s and tier %s for VCore database %s",
            family,
            tier,
            database.name,
        )
        price_per_hour = (
            PROVISIONED_PRICING.get(tier, {}).get(family, {}).get(capacity, basic_price)
        )

    logger.info("Price per hour for the database %s: %s", database.name, price_per_hour)
    monthly_cost = price_per_hour * HOURS_IN_MONTH
    logger.info("Monthly cost for the database %s: %s", database.name, monthly_cost)

    return monthly_cost


def get_single_sql_database_orphan_cost(
    database: Database, monitor_client: MonitorManagementClient
) -> float:
    """Get estimated unnecessary expense done till now from when it was orphaned for a single
    database.

    Args:
    ----
        database (Database): Database object with details.
        monitor_client (MonitorManagementClient): Monitor Management Client object.

    Returns:
    -------
        float: Estimated unnecessary expense done till now from when it was orphaned.

    """
    resource_id: str = database.id  # type: ignore  # noqa: PGH003
    logger.info("Resource Id for Single Database: %s", resource_id)

    activity_logs = get_activity_log_with_resource_id(resource_id, monitor_client)
    monthly_cost = get_single_database_monthly_cost(database)

    if not activity_logs:
        # Resource has been orphaned for at least 90 days
        return round(monthly_cost * 3, 2)

    # Sort the event timestamps so recent is the last item.
    event_times = sorted([event.event_timestamp for event in activity_logs])  # type: ignore  # noqa: PGH003
    logger.info("Event timestamps for the resource %s: %s", resource_id, event_times)

    most_recent_activity_at: datetime = event_times[-1]
    now = datetime.now(UTC)
    logger.info("Most recent activity at: %s", most_recent_activity_at)
    logger.info("Current time: %s", now)
    no_activity_for_days = (now - most_recent_activity_at).days + 1
    # 1 is added because resource minimum billing period is 1 day
    logger.info("No activity for days: %s", no_activity_for_days)

    orphaned_cost = monthly_cost * no_activity_for_days / 30
    logger.info(
        "Orphaned cost for Single Database %s: %s", database.name, orphaned_cost
    )
    return round(orphaned_cost, 2)


def get_container_registry_monthly_cost(registry: Registry) -> float:
    """Get monthly expenditure for a container registry.

    Args:
    ----
        registry (Registry): Container Registry of Azure.

    Returns:
    -------
        float: Monthly cost of the container registry.

    """
    registry_sku: SkuName = registry.sku.name  # type: ignore  # noqa: PGH003
    logger.info(
        "Registry SKU for the container registry %s: %s", registry.name, registry_sku
    )
    price_per_day = azure_pricing.CONTAINER_REGISTRY_PRICING.get(registry_sku, 0.156)
    logger.info(
        "Price per day for the container registry %s: %s", registry.name, price_per_day
    )
    monthly_cost = price_per_day * 30
    logger.info(
        "Monthly cost for the container registry %s: %s", registry.name, monthly_cost
    )
    return round(monthly_cost, 2)


def get_container_registry_orphaned_cost(
    registry: Registry, monitor_client: MonitorManagementClient
) -> float:
    """Get estimated unnecessary expense done till now from when it was orphaned for a container
    registry.

    Args:
    ----
        registry (Registry): Container Registry object with details.

    Returns:
    -------
        float: Estimated unnecessary expense done till now from when it was orphaned.

    """
    resource_id: str = registry.id  # type: ignore  # noqa: PGH003
    logger.info("Resource Id for Container Registry: %s", resource_id)

    activity_logs = get_activity_log_with_resource_id(resource_id, monitor_client)
    monthly_cost = get_container_registry_monthly_cost(registry)

    if not activity_logs:
        # Resource has been orphaned for at least 90 days
        return round(monthly_cost * 3, 2)

    # Sort the event timestamps so recent is the last item.
    event_times = sorted([event.event_timestamp for event in activity_logs])  # type: ignore  # noqa: PGH003
    logger.info("Event timestamps for the resource %s: %s", resource_id, event_times)

    most_recent_activity_at: datetime = event_times[-1]
    now = datetime.now(UTC)
    logger.info("Most recent activity at: %s", most_recent_activity_at)
    no_activity_for_days = (now - most_recent_activity_at).days + 1
    # 1 is added because resource minimum billing period is 1 day
    logger.info("No activity for days: %s", no_activity_for_days)

    orphaned_cost = monthly_cost * no_activity_for_days / 30
    logger.info(
        "Orphaned cost for Container Registry %s: %s", registry.name, orphaned_cost
    )
    return round(orphaned_cost, 2)