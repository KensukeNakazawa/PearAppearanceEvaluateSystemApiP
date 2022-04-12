from typing import List

from src.pear_domain.entity.pure_deterioration import PureDeterioration
from src.pear_domain.value_object.pear_deterioration_db import PearDeteriorationDb
from src.pear_domain.repository.abstract_repository import AbstractRepository


class DeteriorationRepository(AbstractRepository):

    def __init__(self):
        super().__init__()

    def find_by_deterioration_code(self, code: str) -> PureDeterioration:
        find_by_deterioration_code_query = """
            SELECT pear_deterioration_id, deterioration_name, color_b, color_g, color_r
            FROM pear_deteriorations
            WHERE pear_deteriorations.code  = '{code}'
            LIMIT 1
        """.format(code=code)

        rows = self.db.execute(find_by_deterioration_code_query)
        row = rows[0]
        pure_deterioration = PureDeterioration(
            deterioration_id=row[0],
            deterioration_name=row[1],
            color_b=row[2],
            color_g=row[3],
            color_r=row[4]
        )
        return pure_deterioration

    def get_deterioration_by_pear_id(self, pear_id: int) -> List[PearDeteriorationDb]:
        get_query = """
            SELECT 
                pd.deterioration_name, 
                pd.code,
                SUM(sopd.ratio) 
            FROM pears
            INNER JOIN evaluated_side_of_pears AS esop
            ON pears.pear_id = esop.pear_id
            INNER JOIN side_of_pear_deteriorations AS sopd
            ON esop.evaluated_side_of_pear_id = sopd.evaluated_side_of_pear_id
            INNER JOIN pear_deteriorations AS pd
            ON sopd.pear_deterioration_id = pd.pear_deterioration_id
            WHERE pears.pear_id = '{pear_id}'
            GROUP BY sopd.pear_deterioration_id
        """.format(pear_id=pear_id)
        rows = self.db.execute(get_query)
        pear_deteriorations = []
        for row in rows:
            pear_deterioration_db = PearDeteriorationDb(
                name=row[0],
                code=row[1],
                ratio=row[2]
            )
            pear_deteriorations.append(pear_deterioration_db)
        return pear_deteriorations



