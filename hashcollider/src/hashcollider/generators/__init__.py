from hashcollider.generators.random import RandomGenerator
from hashcollider.generators.sequential import SequentialGenerator
from hashcollider.generators.structured import StructuredGenerator

GENERATORS = {
    "random": RandomGenerator,
    "sequential": SequentialGenerator,
    "structured": StructuredGenerator,
}


def get_generator(name: str, **kwargs):
    """Instantiate a generator by name with keyword arguments."""
    try:
        cls = GENERATORS[name]
    except KeyError as exc:
        supported = ", ".join(sorted(GENERATORS))
        raise ValueError(f"Unsupported generator '{name}'. Supported: {supported}") from exc
    return cls(**kwargs)


__all__ = ["RandomGenerator", "SequentialGenerator", "StructuredGenerator",
           "GENERATORS", "get_generator"]
