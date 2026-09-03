import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "creatorflow.db"
LOG_PATH = LOG_DIR / "creatorflow.log"

load_dotenv(ENV_FILE, override=True)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "").strip()

if not DISCORD_TOKEN:
    raise RuntimeError(
        "DISCORD_TOKEN fehlt in der .env-Datei."
    )

if DISCORD_TOKEN.startswith("Bot "):
    raise RuntimeError(
        "DISCORD_TOKEN darf nicht mit 'Bot ' beginnen."
    )


OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY",
    ""
).strip()

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-5.6-luna"
).strip()
