import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime


@dataclass
class ErrorArtifact:
    """Core error record model."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    trace_id: str = ""
    span_id: str = ""
    service: str = "llm-demo"
    env: str = "dev"
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    severity: str = "ERROR"
    exception_type: str = ""
    message: str = ""
    stack: str = ""
    klass: str = ""
    decision: dict = field(default_factory=dict)
    operation: dict = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, ensure_ascii=False)
