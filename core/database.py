import sqlite3
from datetime import datetime, timezone

from core.config import DB_PATH


def connect():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    with connect() as db:
        # ---------------------------------------------
        # Creator Profiles
        # ---------------------------------------------
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS creator_profiles (
                guild_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                creator_level TEXT NOT NULL
                    DEFAULT 'Starter',
                automation_status TEXT NOT NULL
                    DEFAULT 'Active',
                created_at TEXT NOT NULL,
                PRIMARY KEY (guild_id, user_id)
            )
            """
        )

        # ---------------------------------------------
        # AutoVoice Channels
        # ---------------------------------------------
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS autovoice_channels (
                guild_id INTEGER NOT NULL,
                channel_id INTEGER PRIMARY KEY,
                owner_id INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        db.commit()


def get_or_create_profile(
    guild_id: int,
    user_id: int
):
    created_at = datetime.now(
        timezone.utc
    ).isoformat()

    with connect() as db:
        db.execute(
            """
            INSERT OR IGNORE INTO creator_profiles (
                guild_id,
                user_id,
                created_at
            )
            VALUES (?, ?, ?)
            """,
            (
                guild_id,
                user_id,
                created_at,
            ),
        )

        row = db.execute(
            """
            SELECT *
            FROM creator_profiles
            WHERE guild_id = ?
              AND user_id = ?
            """,
            (
                guild_id,
                user_id,
            ),
        ).fetchone()

        db.commit()

    return dict(row)


def register_autovoice_channel(
    guild_id: int,
    channel_id: int,
    owner_id: int
):
    created_at = datetime.now(
        timezone.utc
    ).isoformat()

    with connect() as db:
        db.execute(
            """
            INSERT OR REPLACE INTO autovoice_channels (
                guild_id,
                channel_id,
                owner_id,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                guild_id,
                channel_id,
                owner_id,
                created_at,
            ),
        )
        db.commit()


def remove_autovoice_channel(channel_id: int):
    with connect() as db:
        db.execute(
            """
            DELETE FROM autovoice_channels
            WHERE channel_id = ?
            """,
            (channel_id,),
        )
        db.commit()


def is_autovoice_channel(channel_id: int) -> bool:
    with connect() as db:
        row = db.execute(
            """
            SELECT channel_id
            FROM autovoice_channels
            WHERE channel_id = ?
            """,
            (channel_id,),
        ).fetchone()

    return row is not None


def get_owner_autovoice_channel(
    guild_id: int,
    owner_id: int
):
    with connect() as db:
        row = db.execute(
            """
            SELECT *
            FROM autovoice_channels
            WHERE guild_id = ?
              AND owner_id = ?
            """,
            (
                guild_id,
                owner_id,
            ),
        ).fetchone()

    if row is None:
        return None

    return dict(row)


def migrate_creator_profiles():
    with connect() as db:
        columns = {
            row["name"]
            for row in db.execute(
                "PRAGMA table_info(creator_profiles)"
            ).fetchall()
        }

        migrations = {
            "platform": "TEXT DEFAULT 'Twitch'",
            "niche": "TEXT DEFAULT 'Gaming'",
            "tone": "TEXT DEFAULT 'Casual'",
            "posts_per_week": "INTEGER DEFAULT 5",
        }

        for column, definition in migrations.items():
            if column not in columns:
                db.execute(
                    f"""
                    ALTER TABLE creator_profiles
                    ADD COLUMN {column} {definition}
                    """
                )

        db.commit()


def update_creator_settings(
    guild_id: int,
    user_id: int,
    platform: str,
    niche: str,
    tone: str,
    posts_per_week: int,
):
    get_or_create_profile(
        guild_id,
        user_id,
    )

    with connect() as db:
        db.execute(
            """
            UPDATE creator_profiles
            SET platform = ?,
                niche = ?,
                tone = ?,
                posts_per_week = ?
            WHERE guild_id = ?
              AND user_id = ?
            """,
            (
                platform,
                niche,
                tone,
                posts_per_week,
                guild_id,
                user_id,
            ),
        )

        db.commit()


def get_creator_settings(
    guild_id: int,
    user_id: int,
):
    with connect() as db:
        row = db.execute(
            """
            SELECT *
            FROM creator_profiles
            WHERE guild_id = ?
              AND user_id = ?
            """,
            (
                guild_id,
                user_id,
            ),
        ).fetchone()

    if row is None:
        return None

    return dict(row)
