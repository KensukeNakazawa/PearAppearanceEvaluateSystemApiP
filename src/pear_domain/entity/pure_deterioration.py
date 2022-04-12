from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class PureDeterioration:
    """
    notice: 純粋にDBから汚損データを取得したときのオブジェクト，deteriorationは洋ナシの中から検査された汚損のことなので，混同しないようにする
    """
    deterioration_id: int
    deterioration_name: int
    color_b: int
    color_g: int
    color_r: int

    def get_color_bgr(self) -> Tuple[int, int, int]:
        return self.color_b, self.color_g, self.color_r
