from functools import lru_cache
from datetime import date

from dotenv import load_dotenv

load_dotenv()

from strands import Agent
from strands.agent.conversation_manager.null_conversation_manager import (
    NullConversationManager
)
from bedrock_agentcore.runtime import BedrockAgentCoreApp

from model.load import load_model
from parse import parse_payload
from memory.session import get_memory_session_manager

from agent.prompts import build_system_prompt
from tools.sales_data import get_sales_data
from tools.sales_analysis import get_product_sales_ranking


tools = [
    get_sales_data,
    get_product_sales_ranking
]

DEFAULT_SYSTEM_PROMPT = build_system_prompt(
    date.today().isoformat()
)


def _make_conversation_manager():
    return NullConversationManager()


@lru_cache(maxsize=128)
def _get_agent(session_id: str, actor_id: str) -> Agent:
    """Create or retrieve the Sales Insight Agent."""

    return Agent(
        model=load_model(),
        session_manager=get_memory_session_manager(session_id, actor_id),
        conversation_manager=_make_conversation_manager(),
        system_prompt=DEFAULT_SYSTEM_PROMPT,
        tools=tools,
    )


def create_app():
    app = BedrockAgentCoreApp()
    log = app.logger

    @app.entrypoint
    async def invoke(payload, context):
        log.info("Invoking Sales Insight Agent...")

        session_id = getattr(context, "session_id", None) or "default-session"
        prompt, actor_id = parse_payload(payload)

        log.info(
            f"Invoking with session_id={session_id} "
            f"and actor_id={actor_id}"
        )

        agent = _get_agent(session_id, actor_id)

        async for event in agent.stream_async(prompt):
            if not isinstance(event, dict) or "event" not in event:
                continue

            cbs = event["event"].get("contentBlockStart")

            if cbs is not None and not cbs.get("start"):
                continue

            yield event

    return app


app = create_app()


if __name__ == "__main__":
    app.run()