import json
import logging

from openai import AsyncOpenAI

from core.config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
)


logger = logging.getLogger(
    "creatorflow.ai"
)


class CreatorFlowAIError(Exception):
    pass


def get_client():
    if not OPENAI_API_KEY:
        raise CreatorFlowAIError(
            "OPENAI_API_KEY ist nicht konfiguriert."
        )

    return AsyncOpenAI(
        api_key=OPENAI_API_KEY
    )


def build_content_prompt(settings: dict) -> str:
    platform = settings.get(
        "platform",
        "Twitch"
    )

    niche = settings.get(
        "niche",
        "Gaming"
    )

    tone = settings.get(
        "tone",
        "Casual"
    )

    posts = int(
        settings.get(
            "posts_per_week",
            5
        )
    )

    return f"""
You are the content strategist inside CreatorFlow,
a creator automation platform.

Create a practical weekly content plan for this creator.

CREATOR PROFILE
Platform: {platform}
Niche: {niche}
Tone: {tone}
Posts per week: {posts}

GOAL
Create content that feels native to the creator's niche,
encourages community interaction and can realistically
be produced by a small creator.

RULES
- Create exactly {posts} content items.
- Do not use generic motivational filler.
- Make every idea specific to the niche.
- Keep captions natural and usable.
- Avoid excessive hashtags.
- Use different content formats.
- Include community interaction where appropriate.
- Do not promise guaranteed growth or engagement.
- Output valid JSON only.
- Do not use markdown code fences.

Return this exact structure:

{{
  "strategy": "one short sentence",
  "items": [
    {{
      "day": "Monday",
      "content_type": "Community Post",
      "hook": "short hook",
      "idea": "specific content concept",
      "caption": "ready-to-use caption",
      "cta": "short call to action"
    }}
  ]
}}
""".strip()


async def generate_content_plan(
    settings: dict
) -> dict:
    client = get_client()

    prompt = build_content_prompt(
        settings
    )

    logger.info(
        "Generating AI content plan with %s",
        OPENAI_MODEL,
    )

    try:
        response = await client.responses.create(
            model=OPENAI_MODEL,
            input=prompt,
        )

    except Exception as exc:
        logger.exception(
            "OpenAI request failed"
        )

        raise CreatorFlowAIError(
            "Die AI-Anfrage ist fehlgeschlagen."
        ) from exc

    output = response.output_text.strip()

    if not output:
        raise CreatorFlowAIError(
            "Die AI hat keine Antwort geliefert."
        )

    try:
        data = json.loads(output)

    except json.JSONDecodeError as exc:
        logger.error(
            "Invalid AI JSON: %s",
            output[:1000],
        )

        raise CreatorFlowAIError(
            "Die AI-Antwort konnte nicht verarbeitet werden."
        ) from exc

    if not isinstance(
        data.get("items"),
        list
    ):
        raise CreatorFlowAIError(
            "Ungültiges Content-Plan-Format."
        )

    return data


def generate_fallback_content_plan(
    settings: dict
) -> dict:
    platform = settings.get(
        "platform",
        "Twitch"
    )

    niche = settings.get(
        "niche",
        "Gaming"
    )

    tone = settings.get(
        "tone",
        "Casual"
    )

    posts = int(
        settings.get(
            "posts_per_week",
            5
        )
    )

    templates = [
        {
            "day": "Monday",
            "content_type": "Community Post",
            "hook": f"Let's talk about {niche}",
            "idea": (
                f"Ask your {platform} community a "
                f"specific question about {niche}."
            ),
            "caption": (
                f"Quick {niche} question for the "
                "community today."
            ),
            "cta": "Drop your answer below.",
        },
        {
            "day": "Tuesday",
            "content_type": "Behind the Scenes",
            "hook": "What viewers normally don't see",
            "idea": (
                f"Show part of the process behind "
                f"your {niche} content."
            ),
            "caption": (
                "A little look behind the scenes "
                "before the finished content."
            ),
            "cta": "Want to see more of this?",
        },
        {
            "day": "Wednesday",
            "content_type": "Short / Clip",
            "hook": "This moment deserved its own clip",
            "idea": (
                f"Turn a memorable {niche} moment "
                "into short-form content."
            ),
            "caption": (
                "Some moments are too good "
                "to leave in the full stream."
            ),
            "cta": "Rate this moment from 1-10.",
        },
        {
            "day": "Thursday",
            "content_type": "Opinion Post",
            "hook": f"My take on {niche}",
            "idea": (
                f"Share an authentic opinion about "
                f"a topic inside {niche}."
            ),
            "caption": (
                "This might divide the community, "
                "but here is my take."
            ),
            "cta": "Agree or disagree?",
        },
        {
            "day": "Friday",
            "content_type": "Weekly Highlight",
            "hook": "Best moment of the week",
            "idea": (
                f"Highlight one strong moment from "
                f"your latest {niche} content."
            ),
            "caption": (
                "One of my favorite moments "
                "from this week."
            ),
            "cta": "What was your favorite?",
        },
        {
            "day": "Saturday",
            "content_type": "Community Challenge",
            "hook": "Your turn",
            "idea": (
                f"Create a simple challenge related "
                f"to {niche}."
            ),
            "caption": (
                "Think you can do better? "
                "Show me."
            ),
            "cta": "Try it and share your result.",
        },
        {
            "day": "Sunday",
            "content_type": "Next Week Teaser",
            "hook": "Next week is going to be interesting",
            "idea": (
                f"Tease upcoming {niche} content "
                f"on {platform}."
            ),
            "caption": (
                "A little preview of what is "
                "coming next."
            ),
            "cta": "What do you want to see next?",
        },
    ]

    return {
        "strategy": (
            f"A reliable {tone} content plan for "
            f"{platform} focused on {niche}."
        ),
        "items": templates[:min(posts, 7)],
    }
