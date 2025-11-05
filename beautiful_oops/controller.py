class FaultController:
    """Classify exceptions and decide next actions."""

    def classify(self, exc: Exception) -> str:
        if isinstance(exc, TimeoutError):
            return "Transient"
        if isinstance(exc, ConnectionError):
            return "Upstream"
        if isinstance(exc, ValueError):
            return "Validation"
        return "Fatal"

    def decide(self, klass: str, attempt: int, max_attempts: int) -> dict:
        if klass == "Transient" and attempt < max_attempts:
            return {"action": "retry", "backoff_ms": 500 * attempt}
        if klass in ("Upstream", "Transient"):
            return {"action": "fallback", "fallback_to": "cached_answer"}
        if klass == "Validation":
            return {"action": "ignore"}
        return {"action": "escalate"}
