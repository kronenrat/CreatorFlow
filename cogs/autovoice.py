import logging
import re

import discord
from discord.ext import commands

from core.database import (
    get_owner_autovoice_channel,
    is_autovoice_channel,
    register_autovoice_channel,
    remove_autovoice_channel,
)

logger = logging.getLogger("creatorflow.autovoice")

TRIGGER_NAME = "➕・Create Voice"


def clean_name(name: str) -> str:
    name = re.sub(r"[\n\r\t]", "", name)
    return name[:60]


class AutoVoice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        if member.bot:
            return

        # User joins the Create Voice trigger
        if (
            after.channel is not None
            and after.channel.name == TRIGGER_NAME
        ):
            guild = member.guild

            logger.info(
                "AutoVoice Trigger: %s (%s)",
                member,
                member.id,
            )

            existing = get_owner_autovoice_channel(
                guild.id,
                member.id,
            )

            # Existing personal room?
            if existing:
                existing_channel = guild.get_channel(
                    existing["channel_id"]
                )

                if existing_channel:
                    try:
                        await member.move_to(
                            existing_channel
                        )

                        logger.info(
                            "User moved to existing AutoVoice: %s",
                            existing_channel.id,
                        )
                        return

                    except discord.HTTPException:
                        logger.exception(
                            "Move to existing AutoVoice failed"
                        )

                else:
                    remove_autovoice_channel(
                        existing["channel_id"]
                    )

            channel_name = clean_name(
                f"🔊・{member.display_name}'s Room"
            )

            try:
                channel = await guild.create_voice_channel(
                    name=channel_name,
                    category=after.channel.category,
                    reason="CreatorFlow AutoVoice",
                )

            except discord.Forbidden:
                logger.exception(
                    "Missing permission to create Voice Channel"
                )
                return

            register_autovoice_channel(
                guild.id,
                channel.id,
                member.id,
            )

            try:
                await channel.set_permissions(
                    member,
                    manage_channels=True,
                    move_members=True,
                    connect=True,
                    speak=True,
                )

            except discord.Forbidden:
                logger.warning(
                    "Could not assign AutoVoice owner permissions"
                )

            try:
                await member.move_to(channel)

                logger.info(
                    "AutoVoice created: %s (%s)",
                    channel.name,
                    channel.id,
                )

            except discord.Forbidden:
                logger.exception(
                    "Missing permission to move member"
                )

            except discord.HTTPException:
                logger.exception(
                    "Discord error while moving member"
                )

        # Delete empty temporary AutoVoice
        if (
            before.channel is not None
            and is_autovoice_channel(
                before.channel.id
            )
            and len(before.channel.members) == 0
        ):
            channel_id = before.channel.id

            remove_autovoice_channel(
                channel_id
            )

            try:
                await before.channel.delete(
                    reason="CreatorFlow AutoVoice empty"
                )

                logger.info(
                    "Empty AutoVoice deleted: %s",
                    channel_id,
                )

            except discord.HTTPException:
                logger.exception(
                    "AutoVoice deletion failed"
                )

    @commands.Cog.listener()
    async def on_guild_channel_delete(
        self,
        channel,
    ):
        if (
            isinstance(
                channel,
                discord.VoiceChannel
            )
            and is_autovoice_channel(
                channel.id
            )
        ):
            remove_autovoice_channel(
                channel.id
            )


async def setup(bot):
    await bot.add_cog(
        AutoVoice(bot)
    )
