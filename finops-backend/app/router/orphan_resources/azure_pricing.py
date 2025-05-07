from typing import Final, TypeAlias

from azure.mgmt.containerregistry.models import SkuName as ContainerRegistrySkuName
from azure.mgmt.network.models import (
    ApplicationGatewaySkuName,
    VirtualNetworkGatewaySkuName,
)

# All pricing are in Euros and for location of Germany West Central

PricePerHour: TypeAlias = float
PricePerDay: TypeAlias = float

#################### Application Gateway Pricing ####################
# There should be no capacity charges when Application Gateway is orphan


APP_GATEWAY_PRICING: dict[ApplicationGatewaySkuName, PricePerHour] = {
    ApplicationGatewaySkuName.STANDARD_V2: 0.1873,
    ApplicationGatewaySkuName.WAF_V2: 0.3371,
    ApplicationGatewaySkuName.STANDARD_SMALL: 0.0263,
    ApplicationGatewaySkuName.STANDARD_MEDIUM: 0.0734,
    ApplicationGatewaySkuName.STANDARD_LARGE: 0.3352,
    ApplicationGatewaySkuName.WAF_MEDIUM: 0.1321,
    ApplicationGatewaySkuName.WAF_LARGE: 0.4700,
}

#################### Virtual Network Gateway Pricing ####################
# There should be no data transfer charges since the Virtual Network Gateway is orphan
VNET_GATEWAY_PRICING: dict[VirtualNetworkGatewaySkuName, PricePerHour] = {
    VirtualNetworkGatewaySkuName.BASIC: 0.04,
    VirtualNetworkGatewaySkuName.HIGH_PERFORMANCE: 0.459,
    VirtualNetworkGatewaySkuName.STANDARD: 0.178,
    VirtualNetworkGatewaySkuName.ULTRA_PERFORMANCE: 1.751,
    VirtualNetworkGatewaySkuName.VPN_GW1: 0.1779,
    VirtualNetworkGatewaySkuName.VPN_GW2: 0.4588,
    VirtualNetworkGatewaySkuName.VPN_GW3: 1.1703,
    VirtualNetworkGatewaySkuName.VPN_GW4: 1.9661,
    VirtualNetworkGatewaySkuName.VPN_GW5: 3.4172,
    VirtualNetworkGatewaySkuName.VPN_GW1_AZ: 0.3380,
    VirtualNetworkGatewaySkuName.VPN_GW2_AZ: 0.5281,
    VirtualNetworkGatewaySkuName.VPN_GW3_AZ: 1.3463,
    VirtualNetworkGatewaySkuName.VPN_GW4_AZ: 2.2656,
    VirtualNetworkGatewaySkuName.VPN_GW5_AZ: 3.9231,
    VirtualNetworkGatewaySkuName.ER_GW1_AZ: 0.178,
    VirtualNetworkGatewaySkuName.ER_GW2_AZ: 0.459,
    VirtualNetworkGatewaySkuName.ER_GW3_AZ: 1.751,
}


######################### NAT Gateway Pricing #########################
# There should be no data transfer charges since the NAT Gateway is orphan
# Only resources hours are charged
NAT_GATEWAY_PRICING: PricePerHour = 0.04213


######################### Private DNS Zone Pricing #########################
# There should be no data transfer or query charges since the Private DNS Zone is orphan
# Only resources hours are charged
# Pricing for DNS Zone is variable based on the number of zones, so I will be assuming that
# the total number of zones is less than 25.
# Calculated for per day since minimum billing period is 1 day
PRIVATE_DNS_ZONE_PRICING: PricePerDay = 0.469 / 30  # 0.469 is the price per month

######################### SQL Single Database Pricing #########################
DatabaseType: TypeAlias = str
DTU_Capacity: TypeAlias = int
VCore_Capacity: TypeAlias = int

DTU_BASED_SQL_PRICING: dict[DTU_Capacity, PricePerHour] = {
    5: 0.0079,
    10: 0.0236,
    20: 0.0472,
    50: 0.118,
    100: 0.236,
    200: 0.472,
    400: 0.944,
    800: 1.888,
    1600: 3.776,
    3000: 7.0800,
    125: 0.7315,
    250: 1.4629,
    500: 2.9257,
    1000: 5.8513,
    1750: 11.0105,
    4000: 25.1666,
}

# VCore Based Pricing
PricePerCorePerHour: TypeAlias = float
Family: TypeAlias = str
ServiceTier: TypeAlias = str
SERVERLESS_PRICING: dict[Family, dict[ServiceTier, PricePerCorePerHour]] = {
    "GEN5": {
        "GENERAL_PURPOSE": 0.5374,
        "HYPERSCALE": 0.390,
    }
}

# Provisioned Pricing for SQL Single Database (VCore Based)
PROVISIONED_PRICING: dict[
    ServiceTier, dict[Family, dict[VCore_Capacity, PricePerHour]]
] = {
    "GENERAL_PURPOSE": {
        "GEN5": {
            2: 0.501,
            4: 1.002,
            6: 1.503,
            8: 2.003,
            10: 2.504,
            12: 3.005,
            14: 3.505,
            16: 4.006,
            18: 4.507,
            20: 5.007,
            24: 6.009,
            32: 8.012,
            40: 10.014,
            80: 20.028,
            128: 32.045,
        },
        "FSV2": {
            8: 1.850,
            10: 2.312,
            12: 2.774,
            14: 3.237,
            16: 3.699,
            18: 4.161,
            20: 4.624,
            24: 5.548,
            32: 7.397,
            36: 8.322,
            72: 16.643,
        },
    },
    "BUSINESS_CRITICAL": {
        "GEN5": {
            2: 1.330,
            4: 2.659,
            6: 3.989,
            8: 5.317,
            10: 6.646,
            12: 7.976,
            14: 9.305,
            16: 10.634,
            18: 11.963,
            20: 13.292,
            24: 15.951,
            32: 21.267,
            40: 26.583,
            80: 53.167,
            128: 85.067,
        }
    },
    "HYPERSCALE": {
        "GEN5": {
            2: 0.377,
            4: 0.753,
            6: 1.129,
            8: 1.505,
            10: 1.882,
            12: 2.258,
            14: 2.634,
            16: 3.010,
            18: 3.386,
            20: 3.763,
            24: 4.516,
            32: 6.021,
            40: 7.525,
            80: 15.049,
        },
        "DC_SERIES": {
            2: 0.890,
            4: 1.779,
            6: 2.669,
            8: 3.559,
            10: 4.447,
            12: 5.336,
            14: 6.226,
            16: 7.116,
            18: 8.005,
            20: 8.894,
            32: 14.231,
            40: 17.788,
        },
        "PREMIUM_SERIES": {
            2: 0.377,
            4: 0.753,
            6: 1.129,
            8: 1.505,
            10: 1.882,
            12: 2.258,
            14: 2.634,
            16: 3.010,
            18: 3.386,
            20: 3.763,
            24: 4.516,
            32: 6.021,
            40: 7.525,
            80: 15.049,
            128: 24.078,
        },
        "PREMIUM_SERIES_MEMORY_OPTIMISED": {
            2: 0.527,
            4: 1.054,
            6: 1.581,
            8: 2.108,
            10: 2.635,
            12: 3.161,
            14: 3.687,
            16: 4.214,
            18: 4.741,
            20: 5.267,
            24: 6.321,
            32: 8.428,
            40: 10.534,
            64: 16.855,
            80: 21.068,
        },
    },
}

######################### Container Registry Pricing #########################
# There will be no data storage charges since the Container Registry is orphan, i.e. no images
# Only resources per day are charged
CONTAINER_REGISTRY_PRICING: Final[dict[ContainerRegistrySkuName, PricePerDay]] = {
    ContainerRegistrySkuName.BASIC: 0.156,
    ContainerRegistrySkuName.STANDARD: 0.625,
    ContainerRegistrySkuName.PREMIUM: 1.561,
    ContainerRegistrySkuName.CLASSIC: 0.156,
}