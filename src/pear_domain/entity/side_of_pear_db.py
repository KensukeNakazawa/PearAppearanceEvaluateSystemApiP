from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class SideOfPearDb:
    side_of_pear_id: int
    pear_id: int
    image_path: str
    created_at: str
    updated_at: str

