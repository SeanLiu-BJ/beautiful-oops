import asyncio, traceback, time
from .artifact import ErrorArtifact
from .controller import FaultController
from .sink import ConsoleSink


class FaultExecutor:
    """
    Core orchestrator:
      try -> classify -> decide -> act -> emit artifact
    """

    def __init__(self, controller=None, sinks=None):
        self.controller = controller or FaultController()
        self.sinks = sinks or [ConsoleSink()]

    async def _emit(self, artifact: ErrorArtifact):
        for s in self.sinks:
            await s.emit(artifact)

    async def run(self, op, *,
                  trace_id="trace-1",
                  span_id="span-1",
                  op_name="",
                  max_attempts=3,
                  **kwargs):
        attempt = 1
        while attempt <= max_attempts:
            start = time.time()
            try:
                return await op(**kwargs)
            except Exception as e:
                latency = int((time.time() - start) * 1000)
                art = ErrorArtifact(
                    trace_id=trace_id, span_id=span_id,
                    exception_type=type(e).__name__,
                    message=str(e), stack=traceback.format_exc(),
                    operation={"name": op_name, "attempt": attempt, "latency_ms": latency}
                )

                klass = self.controller.classify(e)
                decision = self.controller.decide(klass, attempt, max_attempts)
                art.klass, art.decision = klass, decision
                await self._emit(art)

                action = decision.get("action")
                if action == "retry":
                    backoff = decision.get("backoff_ms", 0)
                    await asyncio.sleep(backoff / 1000)
                    attempt += 1
                    continue
                elif action == "fallback":
                    return {"status": "fallback", "data": "cached_answer"}
                elif action == "ignore":
                    return {"status": "ignored"}
                else:
                    raise
