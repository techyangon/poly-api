import os

from poly.config import Settings


def override_get_settings():
    return Settings(
        db_host=os.getenv("DB_HOST", "localhost"),
        db_name=os.getenv("DB_NAME", "test"),
        db_username=os.getenv("DB_USERNAME", "admin"),
        db_password=os.getenv("DB_PASSWORD", "passwd"),
        db_port=os.getenv("DB_PORT", "5432"),
    )
