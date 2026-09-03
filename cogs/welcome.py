import logging

import discord
from discord import app_commands
from discord.ext import commands


logger = logging.getLogger("creatorflow.welcome")

WELCOME_CHANNEL = "👋・welcome"
COMMUNITY_ROLE = "👤 Community"


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_welcome(
        self,
        member: discord.Member,
        preview: bool = False,
    ):
        guild = member.guild

        channel = discord.utils.get(
            guild.text_channels,
            name=WELCOME_CHANNEL,
        )

        if channel is None:
            logger.warning(
                "Welcome channel not found"
            )
            return False

        role = discord.utils.get(
            guild.roles,
            name=COMMUNITY_ROLE,
        )

        if role is not None and not preview:
            try:
                await member.add_roles(
                    role,
                    reason="CreatorFlow Smart Welcome",
                )

                logger.info(
                    "Community role assigned to %s",
                    member,
                )

            except discord.Forbidden:
                logger.warning(
                    "Community role could not be assigned"
                )

        embed = discord.Embed(
            title=(
                f"👋 Welcome, "
                f"{member.display_name}!"
            ),
            description=(
                f"Welcome to **{guild.name}**.\n\n"
                "CreatorFlow has automatically "
                "prepared your community access."
            ),
            colour=discord.Colour.blurple(),
        )

        embed.set_thumbnail(
            url=member.display_avatar.url
        )

        embed.add_field(
            name="🚀 Start here",
            value=(
                "Explore the server and test "
                "the CreatorFlow automation systems."
            ),
            inline=False,
        )

        embed.add_field(
            name="🎫 Need help?",
            value=(
                "Open a private support ticket "
                "in the Support section."
            ),
            inline=False,
        )

        embed.set_footer(
            text="CreatorFlow • Smart Welcome"
        )

        await channel.send(
            content=member.mention,
            embed=embed,
        )

        return True

    @commands.Cog.listener()
    async def on_member_join(
        self,
        member: discord.Member,
    ):
        if member.bot:
            return

        logger.info(
            "New member joined: %s",
            member,
        )

        await self.send_welcome(
            member
        )

    @app_commands.command(
        name="welcome-preview",
        description="Testet das CreatorFlow Welcome System.",
    )
    @app_commands.guild_only()
    async def welcome_preview(
        self,
        interaction: discord.Interaction,
    ):
        logger.info(
            "Welcome Preview gestartet von %s (%s)",
            interaction.user,
            interaction.user.id,
        )

        try:
            await interaction.response.defer(
                ephemeral=True
            )

            guild = interaction.guild

            if guild is None:
                await interaction.followup.send(
                    "❌ Kein Discord-Server erkannt.",
                    ephemeral=True,
                )
                return

            channel = discord.utils.get(
                guild.text_channels,
                name=WELCOME_CHANNEL,
            )

            if channel is None:
                available = ", ".join(
                    ch.name
                    for ch in guild.text_channels
                )

                logger.error(
                    "Welcome Channel fehlt. Channels: %s",
                    available,
                )

                await interaction.followup.send(
                    (
                        "❌ Der Kanal `👋・welcome` "
                        "wurde nicht gefunden."
                    ),
                    ephemeral=True,
                )
                return

            embed = discord.Embed(
                title=(
                    f"👋 Welcome, "
                    f"{interaction.user.display_name}!"
                ),
                description=(
                    f"Welcome to **{guild.name}**.\n\n"
                    "This is a preview of the "
                    "CreatorFlow Smart Welcome System."
                ),
                colour=discord.Colour.blurple(),
            )

            embed.set_thumbnail(
                url=interaction.user.display_avatar.url
            )

            embed.add_field(
                name="🚀 Community Access",
                value=(
                    "New members can automatically "
                    "receive their community role."
                ),
                inline=False,
            )

            embed.add_field(
                name="🎫 Automated Support",
                value=(
                    "Members can create private "
                    "support tickets automatically."
                ),
                inline=False,
            )

            embed.add_field(
                name="⚡ CreatorFlow",
                value=(
                    "Welcome, roles, tickets and "
                    "community workflows in one system."
                ),
                inline=False,
            )

            embed.set_footer(
                text="CreatorFlow • Smart Welcome Demo"
            )

            await channel.send(
                content=interaction.user.mention,
                embed=embed,
            )

            await interaction.followup.send(
                (
                    "✅ Welcome Preview wurde in "
                    f"{channel.mention} erstellt."
                ),
                ephemeral=True,
            )

            logger.info(
                "Welcome Preview erfolgreich in %s",
                channel.name,
            )

        except Exception:
            logger.exception(
                "Welcome Preview fehlgeschlagen"
            )

            try:
                await interaction.followup.send(
                    (
                        "❌ Beim Welcome Preview ist "
                        "ein Fehler aufgetreten. "
                        "Details stehen im Bot-Log."
                    ),
                    ephemeral=True,
                )
            except Exception:
                pass


async def setup(bot):
    await bot.add_cog(
        Welcome(bot)
    )
