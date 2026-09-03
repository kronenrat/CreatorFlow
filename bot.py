import asyncio
import logging

import discord
from discord.ext import commands

from core.config import DISCORD_TOKEN
from core.database import init_database, migrate_creator_profiles
from core.logging_config import configure_logging


configure_logging()

logger = logging.getLogger("creatorflow")


intents = discord.Intents.default()
intents.guilds = True
intents.members = True


class CreatorFlowBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None,
        )

    async def setup_hook(self):
        logger.info(
            "Initialisiere CreatorFlow..."
        )

        init_database()
        migrate_creator_profiles()
        logger.info("Database ready")

        extensions = [
            "cogs.general",
            "cogs.profiles",
            "cogs.roadmap",
            "cogs.tickets",
            "cogs.autovoice",
            "cogs.welcome",
            "cogs.creator_intelligence",
            "cogs.demo",
            "cogs.showcase",
            "cogs.setup_server",
        ]

        for extension in extensions:
            try:
                await self.load_extension(
                    extension
                )
                logger.info(
                    "Cog loaded: %s",
                    extension
                )
            except Exception:
                logger.exception(
                    "Cog konnte nicht geladen werden: %s",
                    extension
                )

        synced = await self.tree.sync()

        logger.info(
            "%s Slash Commands synchronisiert",
            len(synced)
        )

    async def on_ready(self):
        logger.info(
            "CreatorFlow online als %s",
            self.user
        )

        logger.info(
            "Verbunden mit %s Server(n)",
            len(self.guilds)
        )

        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="Creator Communities 🚀",
        )

        await self.change_presence(
            status=discord.Status.online,
            activity=activity,
        )


async def main():
    bot = CreatorFlowBot()

    async with bot:
        await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
