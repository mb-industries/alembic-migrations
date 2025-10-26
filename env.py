import os
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool, create_engine, inspect
from database.logger import setup_logger
from database.sqla.models import Base
from dotenv import load_dotenv

# Setup logging
logger = setup_logger()
load_dotenv()

# Read all parts of the connection string strictly from env
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

if not all([POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_DB]):
    raise RuntimeError("Missing one or more required POSTGRES_* environment variables.")

DATABASE_URL = (
    f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

logger.debug(f"🔍 Alembic is using DATABASE_URL: {DATABASE_URL}")

# Alembic config setup
config = context.config
fileConfig(config.config_file_name)
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Reflect metadata
logger.debug("🔍 Tables in metadata: %s", list(Base.metadata.tables.keys()))
engine = create_engine(DATABASE_URL)
logger.debug("🔍 Tables in actual DB: %s", inspect(engine).get_table_names())

target_metadata = Base.metadata
for table in Base.metadata.sorted_tables:
    logger.debug(" - %s", table.name)

# Migrations
def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
