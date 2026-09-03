import discord
from discord import app_commands
from discord.ext import commands


ROLE_CONFIG = [
    ("👑 Creator", discord.Colour.gold()),
    ("🛡️ Moderator", discord.Colour.blue()),
    ("⭐ VIP", discord.Colour.purple()),
    ("🔴 Live", discord.Colour.red()),
    ("👤 Community", discord.Colour.green()),
]


SERVER_STRUCTURE = {
    "🚀 START HERE": [
        ("👋・welcome", "text"),
        ("📖・about-creatorflow", "text"),
        ("📜・rules", "text"),
        ("🎭・roles", "text"),
    ],

    "💬 COMMUNITY": [
        ("💬・general", "text"),
        ("🎮・gaming", "text"),
        ("📸・media", "text"),
        ("🤖・bot-commands", "text"),
    ],

    "🎥 CREATOR HUB": [
        ("🔴・stream-live", "text"),
        ("📅・schedule", "text"),
        ("🗺・roadmap", "text"),
        ("📝・changelog", "text"),
    ],

    "🧠 AUTOMATION LAB": [
        ("⚙️・automation-demo", "text"),
        ("🤖・ai-content", "text"),
        ("📊・analytics", "text"),
    ],

    "🎫 SUPPORT": [
        ("🎫・create-ticket", "text"),
        ("❓・faq", "text"),
    ],

    "🔊 VOICE": [
        ("➕・Create Voice", "voice"),
        ("🔊・Community Lounge", "voice"),
    ],

    "🛡️ TEAM": [
        ("🛡️・team-chat", "text"),
        ("📋・logs", "text"),
    ],
}


class ServerSetup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_or_create_role(
        self,
        guild,
        name,
        colour
    ):
        role = discord.utils.get(
            guild.roles,
            name=name
        )

        if role:
            return role

        return await guild.create_role(
            name=name,
            colour=colour,
            reason="CreatorFlow Setup",
        )

    async def get_or_create_category(
        self,
        guild,
        name,
        overwrites=None
    ):
        category = discord.utils.get(
            guild.categories,
            name=name
        )

        if category:
            if overwrites is not None:
                await category.edit(
                    overwrites=overwrites,
                    reason="CreatorFlow Setup",
                )

            return category

        if overwrites is None:
            return await guild.create_category(
                name,
                reason="CreatorFlow Setup",
            )

        return await guild.create_category(
            name,
            overwrites=overwrites,
            reason="CreatorFlow Setup",
        )

    async def get_or_create_channel(
        self,
        guild,
        category,
        name,
        channel_type
    ):
        existing = discord.utils.get(
            guild.channels,
            name=name
        )

        if existing:
            return existing

        if channel_type == "text":
            return await guild.create_text_channel(
                name,
                category=category,
                reason="CreatorFlow Setup",
            )

        return await guild.create_voice_channel(
            name,
            category=category,
            reason="CreatorFlow Setup",
        )

    async def ensure_welcome_message(
        self,
        channel
    ):
        async for message in channel.history(
            limit=20
        ):
            for embed in message.embeds:
                if (
                    embed.title
                    == "🚀 Welcome to CreatorFlow"
                ):
                    return

        embed = discord.Embed(
            title="🚀 Welcome to CreatorFlow",
            description=(
                "**Your community. Automated.**\n\n"
                "CreatorFlow combines Discord "
                "community management with "
                "creator automation and "
                "AI-assisted workflows.\n\n"
                "Explore the demo server and "
                "test the available systems."
            ),
            colour=discord.Colour.blurple(),
        )

        embed.add_field(
            name="🤖 Community Automation",
            value=(
                "Welcome\n"
                "Tickets\n"
                "AutoVoice\n"
                "Roles\n"
                "Stream Alerts"
            ),
            inline=True,
        )

        embed.add_field(
            name="🧠 Creator AI",
            value=(
                "Content Planning\n"
                "Captions\n"
                "Ideas\n"
                "Analytics\n"
                "Workflows"
            ),
            inline=True,
        )

        embed.add_field(
            name="🎯 Goal",
            value=(
                "Less repetitive work.\n"
                "More time for creating."
            ),
            inline=False,
        )

        embed.set_footer(
            text=(
                "CreatorFlow • "
                "Creator Automation System"
            )
        )

        await channel.send(embed=embed)

    @app_commands.command(
        name="setup",
        description=(
            "Erstellt die CreatorFlow "
            "Demo-Serverstruktur."
        ),
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(
        administrator=True
    )
    async def setup_server(
        self,
        interaction: discord.Interaction
    ):
        await interaction.response.defer(
            ephemeral=True
        )

        guild = interaction.guild

        roles = {}

        for name, colour in ROLE_CONFIG:
            roles[name] = (
                await self.get_or_create_role(
                    guild,
                    name,
                    colour,
                )
            )

        team_overwrites = {
            guild.default_role:
                discord.PermissionOverwrite(
                    view_channel=False
                ),

            roles["🛡️ Moderator"]:
                discord.PermissionOverwrite(
                    view_channel=True
                ),

            roles["👑 Creator"]:
                discord.PermissionOverwrite(
                    view_channel=True
                ),
        }

        created_channels = {}

        for category_name, channels \
                in SERVER_STRUCTURE.items():

            overwrites = None

            if category_name == "🛡️ TEAM":
                overwrites = team_overwrites

            category = (
                await self.get_or_create_category(
                    guild,
                    category_name,
                    overwrites,
                )
            )

            for channel_name, channel_type \
                    in channels:

                channel = (
                    await self.get_or_create_channel(
                        guild,
                        category,
                        channel_name,
                        channel_type,
                    )
                )

                created_channels[
                    channel_name
                ] = channel

        welcome = created_channels.get(
            "👋・welcome"
        )

        if isinstance(
            welcome,
            discord.TextChannel
        ):
            await self.ensure_welcome_message(
                welcome
            )

        ticket_channel = created_channels.get(
            "🎫・create-ticket"
        )

        tickets_cog = self.bot.get_cog(
            "Tickets"
        )

        if (
            tickets_cog is not None
            and isinstance(
                ticket_channel,
                discord.TextChannel
            )
        ):
            await tickets_cog.ensure_ticket_panel(
                guild,
                ticket_channel,
            )

        await interaction.followup.send(
            (
                "✅ CreatorFlow Demo wurde "
                "erfolgreich eingerichtet."
            ),
            ephemeral=True,
        )

    @setup_server.error
    async def setup_error(
        self,
        interaction,
        error
    ):
        if isinstance(
            error,
            app_commands.MissingPermissions
        ):
            message = (
                "❌ Du benötigst "
                "Administrator-Rechte."
            )

            if interaction.response.is_done():
                await interaction.followup.send(
                    message,
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    message,
                    ephemeral=True,
                )

            return

        raise error


async def setup(bot):
    await bot.add_cog(ServerSetup(bot))
