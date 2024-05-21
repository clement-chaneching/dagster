from typing import NamedTuple, Optional, Sequence, Mapping

class CloudRunContainerContext(
    NamedTuple(
        "CloudRunContainerContext",
        [
            ("image", str),
            ("command", Optional[Sequence[str]]),
            ("environment", Mapping[str, str]),
            ("memory", str),
            ("cpu", int),
        ],
    )
):
    """Encapsulates configuration that can be applied to a Cloud Run service."""

    def __new__(
        cls,
        image: str,
        command: Optional[Sequence[str]],
        environment: Optional[Mapping[str, str]],
        memory: str = '512Mi',
        cpu: int = 1,
    ):
        return super().__new__(
            cls,
            image=image,
            command=command or [],
            environment=environment or {},
            memory=memory,
            cpu=cpu,
        )

# Example Usage:
context = CloudRunContainerContext(
    image="gcr.io/project-id/image-name:tag",
    command=["python", "app.py"],
    environment={"ENV_VAR": "value"},
    memory="1Gi",
    cpu=2
)

print(context)
