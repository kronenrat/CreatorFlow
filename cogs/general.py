import discord
from discord import app_commands
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="help",
        description="Zeigt die CreatorFlow Funktionen."
    )
    async def help_command(
        self,
        interaction: discord.Interaction
    ):
        embed = discord.Embed(
            title="🚀 CreatorFlow",
            description=(
                "**Creator Automation System**\n\n"
                "Community, Content und "
                "Workflows in einem modularen System."
            ),
            colour=discord.Colour.blurple(),
        )

        embed.add_field(
            name="🏗️ Community",
            value=(
                "`/setup`\n"
                "Serverstruktur automatisieren"
            ),
            inline=True,
        )

        embed.add_field(
            name="👤 Creator",
            value=(
                "`/profile`\n"
                "Creator-Profil anzeigen"
            ),
            inline=True,
        )

        embed.add_field(
            name="🗺️ Development",
            value=(
                "`/roadmap`\n"
                "`/changelog`"
            ),
            inline=True,
        )

        embed.add_field(
            name="🔜 Next",
            value=(
                "🎫 Tickets\n"
                "🔊 AutoVoice\n"
                "👋 Smart Welcome\n"
                "🧠 AI Content Planner"
            ),
            inline=False,
        )

        embed.set_footer(
            text="CreatorFlow • Build 0.1"
        )

        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(General(bot))
