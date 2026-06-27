import asyncio
import os
import sys

from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from google.adk.runners import InMemoryRunner
from google.genai import types


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
