import os


class ArtifactSink:
    async def emit(self, artifact): ...


class ConsoleSink(ArtifactSink):
    async def emit(self, artifact):
        print(f"\n🧩 ErrorArtifact:\n{artifact.to_json()}\n")


class FileSink(ArtifactSink):
    def __init__(self, path="artifacts/"):
        os.makedirs(path, exist_ok=True)
        self.path = path

    async def emit(self, artifact):
        fname = os.path.join(self.path, f"{artifact.id}.json")
        with open(fname, "w") as f:
            f.write(artifact.to_json())
