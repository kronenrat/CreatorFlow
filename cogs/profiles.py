import discord
from discord import app_commands
from discord.ext import commands

from core.database import get_or_create_profile


class Profiles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="profile",
        description="Zeigt dein CreatorFlow Profil."
    )
    @app_commands.guild_only()
    async def profile(
        self,
        interaction: discord.Interaction
    ):
        profile = get_or_create_profile(
            interaction.guild_id,
            interaction.user.id,
        )

        embed = discord.Embed(
            title=f"👤 {interaction.user.display_name}",
            description="CreatorFlow Creator Profile",
            colour=discord.Colour.blurple(),
        )

        embed.set_thumbnail(
            url=interaction.user.display_avatar.url
        )

        embed.add_field(
            name="🎥 Creator Level",
            value=profile["creator_level"],
            inline=True,
        )

        embed.add_field(
            name="⚡ Automation",
            value=profile["automation_status"],
            inline=True,
        )

        embed.add_field(
            name="🧠 CreatorFlow AI",
            value="Coming in Build 0.2",
            inline=False,
        )

        embed.set_footer(
            text="CreatorFlow • Creator Profile"
        )

        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(Profiles(bot))
