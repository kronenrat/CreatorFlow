import logging

import discord
from discord import app_commands
from discord.ext import commands


logger = logging.getLogger(
    "creatorflow.showcase"
)


ABOUT_CHANNEL = "📖・about-creatorflow"
AUTOMATION_CHANNEL = "⚙️・automation-demo"
AI_CHANNEL = "🤖・ai-content"


class Showcase(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def already_exists(
        self,
        channel: discord.TextChannel,
        title: str,
    ) -> bool:
        async for message in channel.history(
            limit=50
        ):
            if not message.embeds:
                continue

            if message.embeds[0].title == title:
                return True

        return False

    async def send_and_pin(
        self,
        channel: discord.TextChannel,
        embed: discord.Embed,
    ):
        exists = await self.already_exists(
            channel,
            embed.title,
        )

        if exists:
            return False

        message = await channel.send(
            embed=embed
        )

        try:
            await message.pin(
                reason="CreatorFlow Showcase"
            )
        except discord.Forbidden:
            logger.warning(
                "Showcase message could not be pinned in %s",
                channel.name,
            )

        return True

    def about_embed(self):
        embed = discord.Embed(
            title="🚀 What is CreatorFlow?",
            description=(
                "**CreatorFlow is a creator automation "
                "platform combining Discord community "
                "management with AI-powered content workflows.**\n\n"
                "The goal is simple: reduce repetitive work "
                "so creators can spend more time creating."
            ),
            colour=discord.Colour.blurple(),
        )

        embed.add_field(
            name="🤖 Community Automation",
            value=(
                "• Automated server setup\n"
                "• Smart welcome system\n"
                "• Automatic community roles\n"
                "• Private support tickets\n"
                "• Dynamic AutoVoice rooms"
            ),
            inline=True,
        )

        embed.add_field(
            name="🧠 Creator Intelligence",
            value=(
                "• Persistent creator profiles\n"
                "• AI content strategy\n"
                "• Weekly content plans\n"
                "• Hooks and ideas\n"
                "• Captions and CTAs"
            ),
            inline=True,
        )

        embed.add_field(
            name="⚙️ Technology",
            value=(
                "`Python` • `Discord API` • `SQLite`\n"
                "`OpenAI` • `Linux VPS` • `Automation`"
            ),
            inline=False,
        )

        embed.add_field(
            name="▶️ Try it yourself",
            value=(
                "Use `/demo` for the full overview.\n\n"
                "Then configure your creator profile with "
                "`/creator-setup` and generate a real "
                "AI content plan using `/content-plan`."
            ),
            inline=False,
        )

        embed.set_footer(
            text=(
                "CreatorFlow Alpha • "
                "A FlowForge Automation Project"
            )
        )

        return embed

    def automation_embed(self):
        embed = discord.Embed(
            title="⚙️ CreatorFlow Automation Lab",
            description=(
                "This server is not a static mockup.\n\n"
                "**The systems below are live and can "
                "be tested directly.**"
            ),
            colour=discord.Colour.blurple(),
        )

        embed.add_field(
            name="1️⃣ Automated Server Setup",
            value=(
                "`/setup`\n"
                "CreatorFlow can build roles, categories "
                "and channels automatically."
            ),
            inline=False,
        )

        embed.add_field(
            name="2️⃣ Smart Community",
            value=(
                "New members can receive welcome messages "
                "and community roles automatically."
            ),
            inline=False,
        )

        embed.add_field(
            name="3️⃣ Ticket Automation",
            value=(
                "Open `🎫・create-ticket` and create "
                "a private support channel using the button."
            ),
            inline=False,
        )

        embed.add_field(
            name="4️⃣ Dynamic AutoVoice",
            value=(
                "Join `➕・Create Voice`.\n"
                "CreatorFlow creates your personal voice "
                "room, moves you inside and deletes it "
                "again when it becomes empty."
            ),
            inline=False,
        )

        embed.add_field(
            name="5️⃣ Creator Intelligence",
            value=(
                "`/creator-setup`\n"
                "Stores your platform, niche, tone and "
                "content frequency.\n\n"
                "`/content-plan`\n"
                "Uses that profile to generate a personalized "
                "AI content strategy."
            ),
            inline=False,
        )

        embed.set_footer(
            text="CreatorFlow • Live Automation Demo"
        )

        return embed

    def ai_embed(self):
        embed = discord.Embed(
            title="🧠 CreatorFlow AI Content Lab",
            description=(
                "CreatorFlow connects persistent creator "
                "profiles with AI-powered content planning."
            ),
            colour=discord.Colour.blurple(),
        )

        embed.add_field(
            name="Step 1 • Configure",
            value=(
                "Run `/creator-setup` and provide:\n\n"
                "📱 Platform\n"
                "🎯 Niche\n"
                "🎭 Tone\n"
                "📅 Posts per week"
            ),
            inline=True,
        )

        embed.add_field(
            name="Step 2 • Generate",
            value=(
                "Run `/content-plan`.\n\n"
                "CreatorFlow reads your saved profile and "
                "builds a personalized weekly strategy."
            ),
            inline=True,
        )

        embed.add_field(
            name="AI Output",
            value=(
                "💡 Strategy\n"
                "📅 Content schedule\n"
                "🪝 Hooks\n"
                "🎬 Content concepts\n"
                "✍️ Captions\n"
                "📣 Calls to action"
            ),
            inline=False,
        )

        embed.add_field(
            name="🛡️ Reliability",
            value=(
                "CreatorFlow includes a local fallback "
                "planner so the workflow can continue even "
                "when the external AI service is unavailable."
            ),
            inline=False,
        )

        embed.add_field(
            name="💡 Demo Tip",
            value=(
                "Try different niches and tones.\n\n"
                "For example:\n"
                "`Twitch • Gaming • Funny`\n"
                "`TikTok • Music • Emotional`\n"
                "`YouTube • Tech • Professional`"
            ),
            inline=False,
        )

        embed.set_footer(
            text="CreatorFlow • AI Creator Intelligence"
        )

        return embed

    @app_commands.command(
        name="showcase-setup",
        description=(
            "Richtet den CreatorFlow Demo Showroom ein."
        ),
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(
        administrator=True
    )
    async def showcase_setup(
        self,
        interaction: discord.Interaction,
    ):
        await interaction.response.defer(
            ephemeral=True
        )

        guild = interaction.guild

        about = discord.utils.get(
            guild.text_channels,
            name=ABOUT_CHANNEL,
        )

        automation = discord.utils.get(
            guild.text_channels,
            name=AUTOMATION_CHANNEL,
        )

        ai_channel = discord.utils.get(
            guild.text_channels,
            name=AI_CHANNEL,
        )

        missing = []

        if about is None:
            missing.append(ABOUT_CHANNEL)

        if automation is None:
            missing.append(AUTOMATION_CHANNEL)

        if ai_channel is None:
            missing.append(AI_CHANNEL)

        if missing:
            await interaction.followup.send(
                (
                    "❌ Folgende Demo-Kanäle fehlen:\n"
                    + "\n".join(missing)
                    + "\n\nFühre zuerst `/setup` aus."
                ),
                ephemeral=True,
            )
            return

        created = 0

        if await self.send_and_pin(
            about,
            self.about_embed(),
        ):
            created += 1

        if await self.send_and_pin(
            automation,
            self.automation_embed(),
        ):
            created += 1

        if await self.send_and_pin(
            ai_channel,
            self.ai_embed(),
        ):
            created += 1

        logger.info(
            "Showcase setup completed in %s",
            guild.id,
        )

        await interaction.followup.send(
            (
                "✅ CreatorFlow Showroom eingerichtet.\n"
                f"Neue Showcase-Nachrichten: **{created}**"
            ),
            ephemeral=True,
        )


async def setup(bot):
    await bot.add_cog(
        Showcase(bot)
    )
