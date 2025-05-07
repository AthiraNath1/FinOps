import base64
import json
import logging

from azure.identity import ClientSecretCredential, DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.mgmt.resource import SubscriptionClient

from router.user_details.encryption_decryption import decode_and_decrypt

# Initialize common clients and configurations
credential = DefaultAzureCredential()
key_vault_url = "https://demo-key-vault2.vault.azure.net/"
secret_client = SecretClient(vault_url=key_vault_url, credential=credential)
subscription_clients = {}  # cache for SubscriptionClient


def get_secret_value(secret_name):
    """Fetch the secret value from the key vault."""
    return secret_client.get_secret(secret_name).value


def get_secret_object(finops_id):
    try:
        secret_suffixes = ["CLIENTID", "CLIENTSECRET", "TENANTID"]
        keys = ["client_id", "client_secret", "tenant_id"]

        return {
            key: get_secret_value(f"{finops_id}-{suffix}")
            for key, suffix in zip(keys, secret_suffixes)
        }

    except Exception:
        logging.exception("Error in get_secret_object")


def set_secret_object(value: str):
    pass


def get_secret_object_aws(finops_id):
    try:
        secret_suffixes = ["ACCESS-KEY-ID", "SECRET-ACCESS-KEY", "REGION"]
        keys = ["aws_access_key_id", "aws_secret_access_key", "region"]

        return {
            key: get_secret_value(f"{finops_id}-{suffix}")
            for key, suffix in zip(keys, secret_suffixes)
        }

    except Exception:
        logging.exception("Error in get_secret_object")





def get_client_by_integration_name(integration_name: str):
    secret_value = get_secret_value(integration_name)
    decoded_value = decode_and_decrypt(secret_value)
    return json.loads(decoded_value)



def get_subscription_list(integration_name):
    try:
        secrets = get_client_by_integration_name(integration_name)

        subscription_credential = ClientSecretCredential(
            tenant_id=secrets["tenant_id"],
            client_id=secrets["client_id"],
            client_secret=secrets["client_secret"],
        )

        # Reuse subscription client if possible
        if integration_name not in subscription_clients:
            subscription_clients[integration_name] = SubscriptionClient(
                subscription_credential,
            )

        subscription_client = subscription_clients[integration_name]
        return [
            {
                "subscription_id": subscription.subscription_id,
                "name": subscription.display_name,
            }
            for subscription in subscription_client.subscriptions.list()
        ]

    except Exception:
        logging.exception("Error in get_subscription_list")



def update_client_secret(key: str, value: str):
    secret_client.set_secret(name=key, value=value)