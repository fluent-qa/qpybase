from dynaconf import Dynaconf
from pydantic import BaseModel
from typing import Type

settings = Dynaconf(
    envar_prefix="fluent",
    settings_file=["configs/settings.toml", "configs/.secrets.toml", "settings.toml"],
    environment=True,
    load_dotenv=True,
    envvar_prefix=False, # custom path for .env file to be loaded
    includes=["../config/custom_settings.toml"],
)

settings.validators.validate()
def ensure_env_settings(conf: Dynaconf, env_name: str):
    env_switcher_key = conf.ENV_SWITCHER_FOR_DYNACONF
    os.environ[env_switcher_key] = env_name
    conf.reload()

def setting_to_model(setting: Dynaconf, model_type: Type[BaseModel]):
    model_value = model_type()
    for model_field in model_type.model_fields:
        setattr(model_value, model_field, getattr(setting, model_field))
    return model_value

## TODO: add change, listen configuration
