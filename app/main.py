import asyncio
import json
import os
import re
import sys
import uuid

from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from google.adk.runners import InMemoryRunner
from google.genai import types

# --- Phase 2.1 test: session-preseed welcome message ---
# Built via get_fast_api_app() per ADK maintainer guidance, instead of the
# bare `adk web` CLI shortcut, so we get a hook point at session creation.
# See .claude/CLAUDE.md for the full test spec.

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_WELCOME_TEXT = "Hi, I'm Heimdall - placeholder welcome text for testing."

# Matches the non-deprecated "create session" endpoint only:
# POST /apps/{app_name}/users/{user_id}/sessions
# (the deprecated .../sessions/{session_id} variant has no `events` field
# on its request body, so it can't carry a preseeded event).
_SESSION_CREATE_RE = re.compile(r"^/apps/[^/]+/users/[^/]+/sessions$")


def build_web_app():
    from fastapi import Request
    from google.adk.cli.fast_api import get_fast_api_app

    app = get_fast_api_app(agents_dir=_PROJECT_ROOT, web=True)

    @app.middleware("http")
    async def preseed_welcome_message(request: Request, call_next):
        if request.method == "POST" and _SESSION_CREATE_RE.match(
            request.url.path
        ):
            body_bytes = await request.body()
            try:
                payload = json.loads(body_bytes) if body_bytes else {}
            except json.JSONDecodeError:
                payload = {}

            if not payload.get("events"):
                payload["events"] = [
                    {
                        # Real agent turns use the agent's own name as
                        # author, not the literal string "model" - matching
                        # that in case the dev UI keys bot-bubble styling
                        # off it.
                        "author": "HeimdallAgent",
                        "content": {
                            "role": "model",
                            "parts": [{"text": _WELCOME_TEXT}],
                        },
                        # Dev UI's chat-tree builder drops any non-"user"
                        # event with an empty nodeInfo.path.
                        "node_info": {"path": "HeimdallAgent"},
                        # Dev UI groups the whole event list by invocation
                        # and only creates a visible bubble group for
                        # invocations with a non-empty id - a real event
                        # never has an empty one, so match that shape.
                        "invocation_id": f"e-{uuid.uuid4()}",
                    }
                ]
                # Starlette's BaseHTTPMiddleware replays the body it cached
                # on this same request object to the downstream handler, so
                # mutating `_body` in place (rather than swapping in a new
                # Request) is what actually reaches the route.
                request._body = json.dumps(payload).encode()

        return await call_next(request)

    return app


# uvicorn app.main:app
# Only built when imported as an ASGI target, not on `python -m app.main`
# (CLI mode), so the CLI path stays exactly as before.
if __name__ != "__main__":
    app = build_web_app()
# --- end Phase 2.1 test ---


async def run_agent_interactive():
    from app.agent import root_agent

    runner = InMemoryRunner(agent=root_agent, app_name="Heimdall")

    session = await runner.session_service.create_session(
        app_name="Heimdall",
        user_id="local-user",
        state={},
    )

    print("=" * 60)
    print("Heimdall Wholesale Inquiry Triage Agent")
    print("Type your inquiry below. Type 'exit' or 'quit' to end.")
    print("=" * 60)

    while True:
        try:
            query = input("\nUser: ").strip()
            if not query:
                continue
            if query.lower() in ("exit", "quit"):
                break

            new_message = types.Content(role="user", parts=[types.Part(text=query)])

            print("\nAnalyzing...", end="", flush=True)

            response_parts = []
            async for event in runner.run_async(
                user_id=session.user_id,
                session_id=session.id,
                new_message=new_message,
            ):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            response_parts.append(part.text)

            print(f"\r{' '.join(response_parts)}")

        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    if not os.getenv("GEMINI_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
        print("Warning: Neither GEMINI_API_KEY nor GOOGLE_API_KEY is set.")
        print("Check your .env file.")

    asyncio.run(run_agent_interactive())
