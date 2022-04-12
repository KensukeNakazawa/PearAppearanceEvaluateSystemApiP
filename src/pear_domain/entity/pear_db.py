from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class PearDb():
    """
    """
    pear_id: int
    rank_name: str
    area_of_side: float
    created_at: int
    updated_at: int
