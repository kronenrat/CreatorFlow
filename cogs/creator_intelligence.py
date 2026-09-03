import logging

import discord
from discord import app_commands
from discord.ext import commands

from core.ai_content import (
    CreatorFlowAIError,
    generate_content_plan,
    generate_fallback_content_plan,
)
from core.database import (
    get_creator_settings,
    update_creator_settings,
)


logger = logging.getLogger(
    "creatorflow.creator_intelligence"
)


class CreatorIntelligence(
    commands.Cog
):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="creator-setup",
        description=(
            "Konfiguriert dein "
            "CreatorFlow Creator-Profil."
        ),
    )
    @app_commands.describe(
        platform=(
            "Twitch, YouTube, TikTok etc."
        ),
        niche=(
            "Gaming, Music, Tech, Lifestyle etc."
        ),
        tone=(
            "Funny, Casual, Professional etc."
        ),
        posts_per_week=(
            "Anzahl geplanter Posts"
        ),
    )
    @app_commands.guild_only()
    async def creator_setup(
        self,
        interaction: discord.Interaction,
        platform: str,
        niche: str,
        tone: str,
        posts_per_week:
            app_commands.Range[int, 1, 14],
    ):
        update_creator_settings(
            interaction.guild_id,
            interaction.user.id,
            platform.strip(),
            niche.strip(),
            tone.strip(),
            posts_per_week,
        )

        embed = discord.Embed(
            title=(
                "🧠 CreatorFlow "
                "Profile Configured"
            ),
            description=(
                "CreatorFlow now knows the "
                "basic parameters of your brand."
            ),
            colour=discord.Colour.blurple(),
        )

        embed.add_field(
            name="📱 Platform",
            value=platform,
            inline=True,
        )

        embed.add_field(
            name="🎯 Niche",
            value=niche,
            inline=True,
        )

        embed.add_field(
            name="🎭 Tone",
            value=tone,
            inline=True,
        )

        embed.add_field(
            name="📅 Posts / Week",
            value=str(posts_per_week),
            inline=True,
        )

        embed.add_field(
            name="🤖 AI Planning",
            value=(
                "Ready for `/content-plan`"
            ),
            inline=False,
        )

        embed.set_footer(
            text=(
                "CreatorFlow • "
                "Creator Intelligence"
            )
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True,
        )

    @app_commands.command(
        name="content-plan",
        description=(
            "Erstellt einen AI-generierten "
            "Content-Plan."
        ),
    )
    @app_commands.guild_only()
    async def content_plan(
        self,
        interaction: discord.Interaction,
    ):
        settings = get_creator_settings(
            interaction.guild_id,
            interaction.user.id,
        )

        if settings is None:
            await interaction.response.send_message(
                (
                    "❌ Kein Creator-Profil gefunden.\n"
                    "Nutze zuerst `/creator-setup`."
                ),
                ephemeral=True,
            )
            return

        await interaction.response.defer()

        ai_mode = "AI Generated"

        try:
            plan = await generate_content_plan(
                settings
            )

        except CreatorFlowAIError as exc:
            logger.warning(
                "AI unavailable, using fallback: %s",
                exc,
            )

            plan = generate_fallback_content_plan(
                settings
            )

            ai_mode = "Fallback Mode"

        platform = settings.get(
            "platform",
            "Unknown"
        )

        niche = settings.get(
            "niche",
            "Unknown"
        )

        tone = settings.get(
            "tone",
            "Unknown"
        )

        embed = discord.Embed(
            title=(
                "🧠 CreatorFlow "
                "AI Content Plan"
            ),
            description=(
                f"**Platform:** {platform}\n"
                f"**Niche:** {niche}\n"
                f"**Tone:** {tone}\n\n"
                f"💡 **Strategy:** "
                f"{plan.get('strategy', 'Custom weekly plan')}"
            ),
            colour=discord.Colour.blurple(),
        )

        items = plan.get(
            "items",
            []
        )

        if not items:
            await interaction.followup.send(
                (
                    "❌ Die AI hat keinen "
                    "Content geliefert."
                ),
                ephemeral=True,
            )
            return

        for item in items[:14]:
            day = item.get(
                "day",
                "Content"
            )

            content_type = item.get(
                "content_type",
                "Post"
            )

            hook = item.get(
                "hook",
                ""
            )

            idea = item.get(
                "idea",
                ""
            )

            caption = item.get(
                "caption",
                ""
            )

            cta = item.get(
                "cta",
                ""
            )

            value = (
                f"**Hook:** {hook}\n"
                f"**Idea:** {idea}\n"
                f"**Caption:** {caption}\n"
                f"**CTA:** {cta}"
            )

            # Discord Embed Field Limit
            if len(value) > 1000:
                value = (
                    value[:997]
                    + "..."
                )

            embed.add_field(
                name=(
                    f"📅 {day} • "
                    f"{content_type}"
                )[:256],
                value=value,
                inline=False,
            )

        embed.set_footer(
            text=(
                "CreatorFlow • "
                f"Creator Intelligence • {ai_mode}"
            )
        )

        await interaction.followup.send(
            embed=embed
        )

        logger.info(
            "AI Content Plan generated for %s",
            interaction.user.id,
        )


async def setup(bot):
    await bot.add_cog(
        CreatorIntelligence(bot)
    )
