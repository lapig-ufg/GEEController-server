from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix='GEETASK',
    settings_files=['settings.toml', '.secrets.toml','/data/settings.toml','settings.local.toml'],
    environments=True,
    load_dotenv=True,
)