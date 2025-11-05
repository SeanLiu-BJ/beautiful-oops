# 🪞 Beautiful Oops

> **Turning every error into insight**  
> A unified error-capture and decision engine for LLM-driven and agent-based systems.

---

### ✨ Features
- Catch exceptions with full trace metadata
- Classify + Decide + Retry/Fallback automatically
- Emit JSON artifacts (for analysis or Prefect/Opik integration)
- Human-readable, developer-friendly console output

---

### 🧩 Example

```python
from beautiful_oops.executor import FaultExecutor
import asyncio, random

async def unstable_call():
    if random.random() < 0.5:
        raise TimeoutError("API call timed out")
    return "Success!"

async def main():
    executor = FaultExecutor()
    result = await executor.run(unstable_call, op_name="unstable_call")
    print(result)

asyncio.run(main())
