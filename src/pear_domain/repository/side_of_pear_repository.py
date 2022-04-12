from typing import List

from src.pear_domain.entity.side_of_pear_db import SideOfPearDb
from src.pear_domain.repository.abstract_repository import AbstractRepository


class SideOfPearRepository(AbstractRepository):
    def __init__(self):
        super().__init__()

    def get_side_of_pear_by_pear_id(self, pear_id) -> List[SideOfPearDb]:
        get_query = """
            SELECT 
                sop.side_of_pear_id,
                sop.pear_id,
                sop.image_path,
                sop.created_at,
                sop.updated_at
            FROM side_of_pears AS sop
            WHERE sop.pear_id = '{pear_id}'
        """.format(pear_id=pear_id)
        side_of_pears = self.__generate_side_of_pear(get_query)

        return side_of_pears

    def get_evaluated_side_of_pear_by_pear_id(self, pear_id) -> List[SideOfPearDb]:
        get_query = """
            SELECT 
                esop.evaluated_side_of_pear_id,
                esop.pear_id,
                esop.image_path,
                esop.created_at,
                esop.updated_at
            FROM evaluated_side_of_pears AS esop
            WHERE esop.pear_id = '{pear_id}'
        """.format(pear_id=pear_id)
        side_of_pears = self.__generate_side_of_pear(get_query)

        return side_of_pears

    def __generate_side_of_pear(self, get_query: str):
        rows = self.db.execute(get_query)
        side_of_pears = []
        for row in rows:
            side_of_pear_db = SideOfPearDb(
                side_of_pear_id=row[0],
                pear_id=row[1],
                image_path=row[2],
                created_at=row[3],
                updated_at=row[4]
            )
            side_of_pears.append(side_of_pear_db)

        return side_of_pears
