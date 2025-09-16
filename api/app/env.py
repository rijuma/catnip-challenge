import os
from pathlib import Path
from dotenv import load_dotenv

# This loads the env var from the directory in case is run from the terminal instead of the docker container
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DOTENV_PATH = BASE_DIR / ".env"
if DOTENV_PATH.exists():
    load_dotenv(DOTENV_PATH)

DEVELOPMENT = os.getenv("ENV", "dev") == "dev"

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
