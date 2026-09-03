import discord
from discord import app_commands
from discord.ext import commands


class CreatorFlowDemo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="demo",
        description="Zeigt die CreatorFlow Automation Demo.",
    )
    @app_commands.guild_only()
    async def demo(
        self,
        interaction: discord.Interaction,
    ):
        embed = discord.Embed(
            title="🚀 CreatorFlow Automation Platform",
            description=(
                "**Your community. Automated.**\n\n"
                "CreatorFlow combines Discord community "
                "automation with AI-powered creator workflows."
            ),
            colour=discord.Colour.blurple(),
        )

        embed.add_field(
            name="🤖 Community Automation",
            value=(
                "`/setup` Server Setup\n"
                "🎫 Automated Tickets\n"
                "🔊 Dynamic AutoVoice\n"
                "👋 Smart Welcome\n"
                "👤 Automated Roles"
            ),
            inline=True,
        )

        embed.add_field(
            name="🧠 Creator Intelligence",
            value=(
                "`/creator-setup` Creator Profile\n"
                "`/content-plan` AI Content Strategy\n"
                "💡 Content Ideas\n"
                "🪝 Hooks\n"
                "✍️ Captions & CTAs"
            ),
            inline=True,
        )

        embed.add_field(
            name="⚙️ Platform",
            value=(
                "Python • Discord API • SQLite • "
                "OpenAI • Linux VPS"
            ),
            inline=False,
        )

        embed.add_field(
            name="▶️ Try CreatorFlow",
            value=(
                "1. Run `/creator-setup`\n"
                "2. Run `/content-plan`\n"
                "3. Join `➕・Create Voice`\n"
                "4. Create a support ticket"
            ),
            inline=False,
        )

        embed.add_field(
            name="🎯 Purpose",
            value=(
                "Reduce repetitive community and content "
                "work so creators can spend more time creating."
            ),
            inline=False,
        )

        embed.set_footer(
            text="CreatorFlow Alpha • Built by FlowForge"
        )

        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(
        CreatorFlowDemo(bot)
    )
