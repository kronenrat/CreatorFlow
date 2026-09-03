import asyncio
import re

import discord
from discord import app_commands
from discord.ext import commands


TICKET_CATEGORY = "🎫 SUPPORT"
TICKET_CHANNEL = "🎫・create-ticket"

STAFF_ROLES = [
    "🛡️ Moderator",
    "👑 Creator",
]


def safe_channel_name(name: str) -> str:
    name = name.lower()
    name = re.sub(r"[^a-z0-9-]", "-", name)
    name = re.sub(r"-+", "-", name)
    return name.strip("-")[:40] or "user"


class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Close Ticket",
        emoji="🔒",
        style=discord.ButtonStyle.danger,
        custom_id="creatorflow:ticket_close",
    )
    async def close_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        channel = interaction.channel

        if not isinstance(channel, discord.TextChannel):
            return

        topic = channel.topic or ""

        if not topic.startswith("creatorflow-ticket:"):
            await interaction.response.send_message(
                "❌ This channel is not a CreatorFlow ticket.",
                ephemeral=True,
            )
            return

        owner_id_text = topic.split(":")[-1]

        try:
            owner_id = int(owner_id_text)
        except ValueError:
            owner_id = 0

        is_staff = (
            interaction.user.guild_permissions.manage_channels
        )

        if (
            interaction.user.id != owner_id
            and not is_staff
        ):
            await interaction.response.send_message(
                "❌ You are not allowed to close this ticket.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            "🔒 This ticket will be closed in 3 seconds..."
        )

        await asyncio.sleep(3)

        await channel.delete(
            reason="CreatorFlow ticket closed"
        )


class TicketPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Create Ticket",
        emoji="🎫",
        style=discord.ButtonStyle.primary,
        custom_id="creatorflow:ticket_create",
    )
    async def create_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        guild = interaction.guild

        if guild is None:
            return

        await interaction.response.defer(
            ephemeral=True
        )

        marker = (
            f"creatorflow-ticket:"
            f"{interaction.user.id}"
        )

        for channel in guild.text_channels:
            if channel.topic == marker:
                await interaction.followup.send(
                    (
                        "ℹ️ You already have an open ticket: "
                        f"{channel.mention}"
                    ),
                    ephemeral=True,
                )
                return

        category = discord.utils.get(
            guild.categories,
            name=TICKET_CATEGORY,
        )

        if category is None:
            category = await guild.create_category(
                TICKET_CATEGORY,
                reason="CreatorFlow Ticket System",
            )

        overwrites = {
            guild.default_role:
                discord.PermissionOverwrite(
                    view_channel=False
                ),

            interaction.user:
                discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True,
                    attach_files=True,
                    embed_links=True,
                ),
        }

        me = guild.me

        if me is not None:
            overwrites[me] = (
                discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    manage_channels=True,
                    read_message_history=True,
                )
            )

        for role_name in STAFF_ROLES:
            role = discord.utils.get(
                guild.roles,
                name=role_name,
            )

            if role:
                overwrites[role] = (
                    discord.PermissionOverwrite(
                        view_channel=True,
                        send_messages=True,
                        read_message_history=True,
                    )
                )

        username = safe_channel_name(
            interaction.user.display_name
        )

        channel = await guild.create_text_channel(
            name=f"ticket-{username}",
            category=category,
            overwrites=overwrites,
            topic=marker,
            reason="CreatorFlow ticket created",
        )

        embed = discord.Embed(
            title="🎫 CreatorFlow Support",
            description=(
                f"Hi {interaction.user.mention}!\n\n"
                "Please describe your request here. "
                "A team member can assist you directly "
                "in this private channel."
            ),
            colour=discord.Colour.blurple(),
        )

        embed.add_field(
            name="🔒 Private",
            value=(
                "Only you and the CreatorFlow team "
                "can see this ticket."
            ),
            inline=False,
        )

        embed.set_footer(
            text="CreatorFlow • Ticket System"
        )

        await channel.send(
            content=interaction.user.mention,
            embed=embed,
            view=CloseTicketView(),
        )

        await interaction.followup.send(
            (
                "✅ Ticket created: "
                f"{channel.mention}"
            ),
            ephemeral=True,
        )


class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.bot.add_view(TicketPanelView())
        self.bot.add_view(CloseTicketView())

    async def ensure_ticket_panel(
        self,
        guild: discord.Guild,
        channel: discord.TextChannel,
    ):
        async for message in channel.history(
            limit=25
        ):
            if not message.embeds:
                continue

            if (
                message.embeds[0].title
                == "🎫 CreatorFlow Support Center"
            ):
                return

        embed = discord.Embed(
            title="🎫 CreatorFlow Support Center",
            description=(
                "Need help or want to test the "
                "CreatorFlow ticket automation?\n\n"
                "Click the button below to create "
                "your own private support channel."
            ),
            colour=discord.Colour.blurple(),
        )

        embed.add_field(
            name="⚡ Automated",
            value=(
                "CreatorFlow creates the channel, "
                "sets permissions and provides a "
                "private support workflow automatically."
            ),
            inline=False,
        )

        embed.set_footer(
            text="CreatorFlow • Support Automation"
        )

        await channel.send(
            embed=embed,
            view=TicketPanelView(),
        )

    @app_commands.command(
        name="ticket-panel",
        description="Creates the CreatorFlow ticket panel.",
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(
        administrator=True
    )
    async def ticket_panel(
        self,
        interaction: discord.Interaction,
    ):
        channel = discord.utils.get(
            interaction.guild.text_channels,
            name=TICKET_CHANNEL,
        )

        if channel is None:
            await interaction.response.send_message(
                "❌ The ticket channel does not exist.",
                ephemeral=True,
            )
            return

        await self.ensure_ticket_panel(
            interaction.guild,
            channel,
        )

        await interaction.response.send_message(
            "✅ Ticket panel configured.",
            ephemeral=True,
        )


async def setup(bot):
    await bot.add_cog(Tickets(bot))
