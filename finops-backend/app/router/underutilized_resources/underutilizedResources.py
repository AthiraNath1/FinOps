import concurrent.futures
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient,SubscriptionClient
from azure.mgmt.compute import ComputeManagementClient
import datetime
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.web import WebSiteManagementClient
import jwt
from router.user_details.user_details import (
    get_client_by_integration_name,
)


class OrphanedResources:
    def __init__(self, resource_type, resource_name, resource_id, resource_group, location, monthly_utilization_value, metric):
        self.resource_type = resource_type
        self.resource_name = resource_name
        self.resource_id = resource_id
        self.resource_group = resource_group
        self.location = location
        self.monthly_utilization_value = monthly_utilization_value
        self.metric = metric


def sync_list_resource_groups(resource_client, logger):
    try:
        logger.info('inside sync_list_resource_groups function')
        return list(resource_client.resource_groups.list())
    except Exception as e:
        logger.error(f'this is error mode {e}')


def get_underutilized_resources_list(subscription_id, resource_client, compute_client, monitor_client, sql_client, web_mgmt_client, logger):
    try:
        logger.info('inside get_underutilized_resources_list function')
        # print("get_underutilized_resources_list")
        underutilized_resource_list = []
        resource_groups = sync_list_resource_groups(resource_client, logger)
        logger.debug(f'length of resource_groups is {len(resource_groups)}')
        # Use ThreadPool to process resource groups in parallel.
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(lambda rg: process_rg(
                rg, compute_client, monitor_client, sql_client, web_mgmt_client, logger), resource_groups))

        for res in results:
            underutilized_resource_list.extend(res)
        logger.debug(
            f'length of underutilized_resource_list is {len(underutilized_resource_list)}')
        logger.info('get_underutilized_resources_list function executed')
        return underutilized_resource_list
    except Exception as e:
        logger.error(f'this is error mode {e}')


def fetch_underutlized_database(rg, sql_client, monitor_client, logger):
    try:
        # print("fetch_underutlized_database")
        resources = []
        metric_name = 'cpu_percent'
        server_by_resource_group = sql_client.servers.list_by_resource_group(
            rg.name)
        for server in server_by_resource_group:
            # print("server", server.name)
            databases = sql_client.databases.list_by_server(
                rg.name, server.name)
            for database_iterator in databases:
                # print("database_iterator name", database_iterator.name)
                status = database_iterator.status
                resource_id = database_iterator.id
                if (status and status == 'Online'):
                    cpuPercentage = fetch_utilization(
                        resource_id, monitor_client, metric_name, logger)
                    if (cpuPercentage < 5):
                        # print("cpuPercentage < 5")
                        resources.append(OrphanedResources(
                            database_iterator.type, database_iterator.name, database_iterator.id, rg.name, database_iterator.location, cpuPercentage, 'Percentage CPU'))
        return resources
    except Exception as e:
        logger.error(f'this is error mode {e}')


def fetch_underutlized_vm(rg, compute_client, monitor_client, logger):
    try:
        # print("fetch_underutlized_vm")
        resources = []
        metric_name = 'Percentage CPU'
        vms_by_resource_group = compute_client.virtual_machines.list(rg.name)
        for vm in vms_by_resource_group:
            # print("vm.........", vm)
            resource_group = rg.name
            vm_name = vm.name
            resource_id = vm.id
            statuses = compute_client.virtual_machines.instance_view(
                resource_group, vm_name).statuses
            status = len(statuses) >= 2 and statuses[1]
            if (status and status.code == 'PowerState/running'):
                # print("is status is PowerState/running")
                cpuPercentage = fetch_utilization(
                    resource_id, monitor_client, metric_name, logger)
                if (cpuPercentage < 20):
                    # print("cpuPercentage < 20")
                    resources.append(OrphanedResources(
                        vm.type, vm.name, vm.id, rg.name, vm.location, cpuPercentage, metric_name))
        return resources
    except Exception as e:
        logger.error(f'this is error mode {e}')


def fetch_underutlized_web_apps(rg, web_mgmt_client, monitor_client, logger):
    try:
        # print("fetch_underutlized_vm")
        resources = []
        metric_name = 'Requests'
        web_apps_by_resource_group = web_mgmt_client.web_apps.list_by_resource_group(
            rg.name)
        for web_apps_iterator in web_apps_by_resource_group:
            resource_id = web_apps_iterator.id
            status = web_apps_iterator.state
            # print("name XXXXXXXXXXXXXXX", web_apps_iterator.name)
            if (status and status == 'Running'):
                cpuPercentage = fetch_utilization(
                    resource_id, monitor_client, metric_name, logger)
                if (cpuPercentage < 20):
                    # print("cpuPercentage < 20")
                    resources.append(OrphanedResources(
                        web_apps_iterator.type, web_apps_iterator.name, web_apps_iterator.id, rg.name, web_apps_iterator.location, cpuPercentage, metric_name))
        return resources
    except Exception as e:
        logger.error(f'this is error mode {e}')


def fetch_utilization(resource_id, monitor_client, metric, logger):
    try:
        # print("inside fetch_cpu_utilization_vm")
        today = datetime.datetime.now().date()
        month = today - datetime.timedelta(days=30)
        # print("today", today)
        # print("month", month)
        # print("resource_id", resource_id)
        metrics_data = monitor_client.metrics.list(
            resource_id,
            timespan="{}/{}".format(month, today),
            interval='P1D',
            metricnames=metric,
            aggregation='Average'
        )
        utilization_value = 0
        avg_monthly_value = 0
        avg_count = 0
        for item in metrics_data.value:
            for timeserie in item.timeseries:
                for data in timeserie.data:
                    # print("{}: {}".format(data.time_stamp, data.average))
                    if data.average is not None:
                        # print('average...........',data.average)
                        avg_monthly_value += data.average
                        avg_count += 1
                        # print("avg_monthly_value", avg_monthly_value)
                        # print("avg_count", avg_count)
        if (avg_monthly_value is not None and avg_count is not None and avg_count != 0):
            # print('hhghkh',(avg_monthly_value/avg_count))
            utilization_value = round((avg_monthly_value/avg_count), 2)
            # print("utilization_value", utilization_value)
        return utilization_value
    except Exception as e:
        logger.error(f'this is error mode {e}')


def process_rg(rg, compute_client, monitor_client, sql_client, web_mgmt_client, logger):
    try:
        tasks = [
            fetch_underutlized_vm(rg, compute_client, monitor_client, logger),
            fetch_underutlized_database(
                rg, sql_client, monitor_client, logger),
            fetch_underutlized_web_apps(
                rg, web_mgmt_client, monitor_client, logger)
        ]

        resources = [item for sublist in tasks for item in sublist]
        return resources
    except Exception as e:
        logger.error(f'this is error mode {e}')


def generate_underutilized_resources( integration_name,subscription_id, logger):
    try:
        logger.info('inside generate_underutilized_resources function')
        client_secrets = get_client_by_integration_name(integration_name)
        credential = ClientSecretCredential(
            tenant_id=client_secrets["tenant_id"],
            client_id=client_secrets["client_id"],
            client_secret=client_secrets["client_secret"],
        )
       
        logger.info('credentials retrieved')
        resource_client = ResourceManagementClient(credential, subscription_id)
        compute_client = ComputeManagementClient(credential, subscription_id)
        monitor_client = MonitorManagementClient(credential, subscription_id)
        sql_client = SqlManagementClient(credential, subscription_id)
        web_mgmt_client = WebSiteManagementClient(credential, subscription_id)
        
        subscription_client = SubscriptionClient(credential)

        subscription = subscription_client.subscriptions.get(subscription_id)

        
        print(f"Subscription Name: {subscription.display_name}, ID: {subscription.subscription_id}")
        print('list,',resource_client,compute_client,monitor_client,sql_client,web_mgmt_client)
        return get_underutilized_resources_list(subscription_id, resource_client, compute_client, monitor_client, sql_client, web_mgmt_client, logger)
    except Exception as e:
        logger.error(f'this is error mode {e}')