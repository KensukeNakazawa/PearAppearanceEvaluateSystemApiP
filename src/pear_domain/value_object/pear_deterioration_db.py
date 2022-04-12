from dataclasses import dataclass


@dataclass(frozen=True)
class PearDeteriorationDb:
    name: str
    code: str
    ratio: float

