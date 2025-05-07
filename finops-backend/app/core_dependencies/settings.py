from dotenv import load_dotenv
from pydantic import BaseSettings

from router.user_details.dev_details import get_developer_secret_object

secrets = get_developer_secret_object()


class Settings(BaseSettings):
    # Database
    db_driver: str = secrets["DB_DRIVER1"]
    db_host: str = secrets["DB_HOST"]
    db_port: str = secrets["DB_PORT"]
    db_database: str = secrets["DB_DATABASE"]
    db_user: str = secrets["DB_USER"]
    db_password: str = secrets["DB_PASSWORD"]

    class Config:
        _env_file = load_dotenv(".env", override=True)


settings = Settings()