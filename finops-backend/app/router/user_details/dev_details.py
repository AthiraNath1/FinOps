from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
key_vault_url = "https://demo-key-vault2.vault.azure.net"
secret_client = SecretClient(vault_url=key_vault_url, credential=credential)


def get_developer_secret_value(secret_name):
    """Fetch the secret value from the key vault."""
    return secret_client.get_secret(secret_name).value


def get_developer_secret_object():
    secret = [
        "DB-DRIVER1",
        "DB-HOST",
        "DB-PORT",
        "DB-DATABASE",
        "DB-USER",
        "DB-PASSWORD",
    ]

    keys = [
        "DB_DRIVER1",
        "DB_HOST",
        "DB_PORT",
        "DB_DATABASE",
        "DB_USER",
        "DB_PASSWORD",
    ]

    secrets_dict = {}
    for key, secret_name in zip(keys, secret):
        secrets_dict[key] = get_developer_secret_value(secret_name)
    return secrets_dict


def update_developer_secret_object(secret_name, secret_value):
    secret_client.set_secret(secret_name, secret_value)