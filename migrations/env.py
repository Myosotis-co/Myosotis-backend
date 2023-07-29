import asyncio
from logging.config import fileConfig
import os
import sys
from dotenv import load_dotenv
from sqlalchemy import engine_from_config
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import create_engine
from app.database import SQLALCHEMY_DATABASE_URL,Base
from alembic import context
from app.auth.models import metadata as auth_metadata
from app import seeder

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, "docker/env/.env-docker"))
sys.path.append(BASE_DIR)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# this will overwrite the ini-file sqlalchemy.url path
# with the path given in the config of the main code
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

target_metadata = auth_metadata



def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    #seeder.seed(url)
    # seeder.seed(url)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = AsyncEngine(create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True))

    #seeder.seed(connectable)

    async with connectable.connect() as connection:
         await do_run_migrations_online(connection)
        


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
