from os import environ as env
from handlers import logger as logging

def get_env_variable(var_name, default_value=None):
    value = env.get(var_name, default_value)
    if value is None:
        logging.warning(f"Environment VAR {var_name} not found, default value: {default_value}")
    return value


DB_NAME = get_env_variable("POSTGRES_DB")
DB_PORT = get_env_variable("DB_PORT", "5432")
DB_USER = get_env_variable("POSTGRES_USER")
DB_PASS = get_env_variable("POSTGRES_PASSWORD")

APP_PORT = int(get_env_variable("APP_PORT", "8080"))

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@db:{DB_PORT}/{DB_NAME}"
