import logging

from azure.core.exceptions import AzureError
from azure.identity import ClientSecretCredential, DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.mgmt.resource import SubscriptionClient

from router.user_details.user_details import (
    get_client_by_integration_name,
)

# Initialize common clients and configurations
credential = DefaultAzureCredential()
key_vault_url = "https://demo-key-vault2.vault.azure.net/"
secret_client = SecretClient(vault_url=key_vault_url, credential=credential)
_subscription_clients = {}  # cache for SubscriptionClient


def get_secret_value(secret_name):
    """Fetch the secret value from the key vault."""
    print(secret_client.get_secret(secret_name).value)
    return secret_client.get_secret(secret_name).value


def get_secret_object(finops_id):
    try:
        secret_suffixes = ["CLIENTID", "CLIENTSECRET", "TENANTID"]
        keys = ["client_id", "client_secret", "tenant_id"]

        return {
            key: get_secret_value(f"{finops_id}-{suffix}")
            for key, suffix in zip(keys, secret_suffixes)
        }

    except AzureError:
        logging.exception("AzureError in get_secret_object")
        raise


def get_subscription_list(finops_id):
    try:
        secrets = get_client_by_integration_name(integration_name=finops_id)
        print(secrets["tenant_id"],secrets["client_id"],secrets["client_secret"])
        subscription_credential = ClientSecretCredential(
            tenant_id=secrets["tenant_id"],
            client_id=secrets["client_id"],
            client_secret=secrets["client_secret"],
        )

        # Reuse subscription client if possible
        subscription_client = _subscription_clients.get(finops_id)

        if subscription_client is None:
            subscription_client = SubscriptionClient(subscription_credential)
            _subscription_clients[finops_id] = subscription_client

        return [
            {
                "subscription_id": subscription.subscription_id,
                "name": subscription.display_name,
            }
            for subscription in subscription_client.subscriptions.list()
        ]

    except AzureError:
        logging.exception("AzureError in get_subscription_list")
        raise


