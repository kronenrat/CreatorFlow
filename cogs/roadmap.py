import discord
from discord import app_commands
from discord.ext import commands


class Roadmap(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="roadmap",
        description="Zeigt die CreatorFlow Roadmap."
    )
    async def roadmap(
        self,
        interaction: discord.Interaction
    ):
        embed = discord.Embed(
            title="🗺️ CreatorFlow Roadmap",
            description=(
                "Vom Discord-System zur "
                "Creator-Automation-Plattform."
            ),
            colour=discord.Colour.blurple(),
        )

        embed.add_field(
            name="✅ Build 0.1 • Foundation",
            value=(
                "Core Architecture\n"
                "SQLite Profiles\n"
                "Discord Setup\n"
                "Roadmap & Changelog"
            ),
            inline=False,
        )

        embed.add_field(
            name="🔨 Build 0.2 • Community",
            value=(
                "Ticket System\n"
                "AutoVoice\n"
                "Smart Welcome\n"
                "Role Automation"
            ),
            inline=False,
        )

        embed.add_field(
            name="🧠 Build 0.3 • AI",
            value=(
                "AI Content Planner\n"
                "Caption Generator\n"
                "Creator Configuration"
            ),
            inline=False,
        )

        embed.add_field(
            name="📊 Build 0.4 • Intelligence",
            value=(
                "Analytics\n"
                "Weekly Reports\n"
                "Content Optimization"
            ),
            inline=False,
        )

        await interaction.response.send_message(
            embed=embed
        )

    @app_commands.command(
        name="changelog",
        description="Zeigt den CreatorFlow Changelog."
    )
    async def changelog(
        self,
        interaction: discord.Interaction
    ):
        embed = discord.Embed(
            title="📝 CreatorFlow Changelog",
            description=(
                "**Build 0.1 • Foundation**"
            ),
            colour=discord.Colour.green(),
        )

        embed.add_field(
            name="✨ Neu",
            value=(
                "• modularer Bot-Core\n"
                "• Config-System\n"
                "• SQLite-Datenbank\n"
                "• File + Console Logging\n"
                "• Creator Profiles\n"
                "• automatisches Server Setup"
            ),
            inline=False,
        )

        embed.add_field(
            name="🔜 Next",
            value=(
                "Tickets, AutoVoice "
                "und Smart Welcome"
            ),
            inline=False,
        )

        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(Roadmap(bot))
