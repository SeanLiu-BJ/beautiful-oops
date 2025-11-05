import asyncio, random
from beautiful_oops.executor import FaultExecutor


async def mock_llm_api_call(prompt: str):
    """Simulated LLM API with random failures."""
    r = random.random()
    if r < 0.3:
        raise TimeoutError("LLM API timeout")
    elif r < 0.6:
        raise ConnectionError("Gateway unreachable")
    elif r < 0.8:
        raise ValueError("Prompt format invalid")
    return {"status": "ok", "response": "Hello from LLM!"}


async def main():
    executor = FaultExecutor()
    result = await executor.run(
        mock_llm_api_call,
        op_name="call_llm",
        prompt="Generate video title",
        trace_id="demo-trace"
    )
    print("✅ Final result:", result)


if __name__ == "__main__":
    asyncio.run(main())
