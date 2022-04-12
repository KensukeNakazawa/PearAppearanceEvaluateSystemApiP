import os
from typing import List

from config import constants
from src.pear_domain.repository.abstract_repository import AbstractRepository
from src.pear_domain.entity.pear import Pear
from src.pear_domain.entity.pear_db import PearDb
from src.pear_domain.entity.side_of_pear import SideOfPear
from src.utils.image import load_from_s3


class PearRepository(AbstractRepository):
    
    def __init__(self):
        super().__init__()

    def create(self) -> int:
        now = self.get_now()
        create_pear_query = """
            INSERT INTO pears 
                (created_at, updated_at)
            VALUES 
                ('{created_at}', '{updated_at}')
        """.format(created_at=now, updated_at=now)
        self.db.execute(create_pear_query, insert_or_create_flg=True)

        pear_query = """
            SELECT pear_id FROM pears
            ORDER BY pear_id DESC 
            LIMIT 1;
        """
        pear_id = self.db.execute(pear_query)[0][0]

        return pear_id

    def create_side_of_pear(self, pear_id: int, image_paths: List) -> None:
        now = self.get_now()

        if os.getenv('ENVIRONMENT') == 'local':
            local_image_path = constants.PROJECT_ROOT_PATH + '/images/original_images/01/'
            image_paths = [local_image_path + 'Img00016.bmp', local_image_path + 'Img00017.bmp', local_image_path + 'Img00018.bmp']

        create_side_of_pear_query = """
            INSERT INTO side_of_pears 
                (pear_id, image_path, created_at, updated_at)
            VALUES
                ('{pear_id}', '{image_path_1}', '{created_at}', '{updated_at}'),
                ('{pear_id}', '{image_path_2}', '{created_at}', '{updated_at}'),
                ('{pear_id}', '{image_path_3}', '{created_at}', '{updated_at}')
        """.format(pear_id=pear_id,
                   image_path_1=image_paths[0],
                   image_path_2=image_paths[1],
                   image_path_3=image_paths[2],
                   created_at=now,
                   updated_at=now
                   )
        self.db.execute(create_side_of_pear_query, insert_or_create_flg=True)
        return None

    def find_by_id(self, pear_id: int) -> Pear:
        find_pear_query = """
            SELECT 
                pears.pear_id AS pear_id, 
                pears.pear_rank_id, 
                side_of_pears.side_of_pear_id, 
                side_of_pears.image_path
            FROM pears
            INNER JOIN side_of_pears
            ON pears.pear_id = side_of_pears.pear_id
            WHERE pears.pear_id = '{pear_id}'
        """.format(pear_id=pear_id)
        rows = self.db.execute(find_pear_query)

        pear = Pear(pear_id=pear_id, side_of_pears=[], rank_id=0)
        for row in rows:
            image_path = row[3]
            image = load_from_s3(image_path)
            side_of_pear = SideOfPear(
                image=image,
                side_of_pear_id=row[2],
                area=None,
                deteriorations=[],
                contours=None,
                coordinate=None
            )
            side_of_pear.file = image_path
            pear.add_side_of_pear(side_of_pear)
        return pear

    def get_pear_by_id(self, pear_id: int) -> PearDb:
        get_pear_query = """
            SELECT 
                pears.pear_id,
                pr.rank_name,
                pears.area_of_side,
                pears.created_at,
                pears.updated_at
            FROM pears
            INNER JOIN pear_ranks pr
            ON pr.pear_rank_id = pears.pear_rank_id
            WHERE pears.pear_id = '{pear_id}'
        """.format(pear_id=pear_id)

        rows = self.db.execute(get_pear_query)
        row = rows[0]
        return PearDb(
            pear_id=row[0],
            rank_name=row[1],
            area_of_side=row[2],
            created_at=row[3],
            updated_at=row[4]
        )

    def save_pear_at_evaluated(self, pear: Pear, image_paths: List):
        """検査終了後の情報をDBに永続化する
        Args:
            pear:
            image_paths:
        Returns:

        """
        now = self.get_now()

        # 対象のナシを評価済みにする
        update_pear_query = """
            UPDATE pears
            SET pear_rank_id = '{pear_rank_id}'
            WHERE pear_id = '{pear_id}';
        """.format(pear_rank_id=pear.rank_id, pear_id=pear.pear_id)
        self.db.execute(update_pear_query, insert_or_create_flg=True)

        # evaluated_pearを作成する
        insert_evaluated_side_of_pear_query = """
            INSERT INTO evaluated_side_of_pears 
                (pear_id, image_path, created_at, updated_at)
            VALUES
            
        """
        insert_evaluated_side_of_pear_query_values = []
        for index, side_of_pear in enumerate(pear.side_of_pears):
            insert_evaluated_side_of_pear_query_values.append(
                """
                ('{pear_id}', '{image_path}', '{created_at}', '{updated_at}')
                """.format(pear_id=pear.pear_id, image_path=image_paths[index], created_at=now, updated_at=now)
            )
        insert_evaluated_side_of_pear_query += ', '.join(insert_evaluated_side_of_pear_query_values)
        self.db.execute(insert_evaluated_side_of_pear_query, insert_or_create_flg=True)

        # このあとのdeteriorationの保存に必要な評価済みの側面のIDをしてリストに詰める
        get_evaluated_evaluated_side_of_pear_query = """
            SELECT evaluated_side_of_pears.evaluated_side_of_pear_id
            FROM evaluated_side_of_pears
            WHERE evaluated_side_of_pears.pear_id = '{pear_id}'
        """.format(pear_id=pear.pear_id)
        rows = self.db.execute(get_evaluated_evaluated_side_of_pear_query)
        evaluated_side_of_pear_ids = []
        for row in rows:
            evaluated_side_of_pear_ids.append(int(row[0]))

        # 汚損状況を保存する
        insert_side_of_pear_deterioration_query = """
            INSERT INTO side_of_pear_deteriorations
                (
                    evaluated_side_of_pear_id, pear_deterioration_id, ratio,
                    top_y, left_x, under_y, right_x,
                    created_at, updated_at
                )
            VALUES
                
        """
        insert_side_of_pear_deterioration_query_values = []
        for index, side_of_pear in enumerate(pear.side_of_pears):
            for deterioration in side_of_pear.deteriorations:
                insert_side_of_pear_deterioration_query_values.append(
                    """
                        (
                            '{evaluated_side_of_pear_id}', '{pear_deterioration_id}', '{ratio}',
                            '{top}', '{left}', '{under}', '{right}', 
                            '{created_at}', '{updated_at}'
                        )
                    """.format(
                        evaluated_side_of_pear_id=evaluated_side_of_pear_ids[index],
                        pear_deterioration_id=deterioration.pear_deterioration_id,
                        ratio=deterioration.area_rate,
                        top=deterioration.coordinate.top,
                        left=deterioration.coordinate.left,
                        under=deterioration.coordinate.under,
                        right=deterioration.coordinate.right,
                        created_at=now,
                        updated_at=now
                    )
                )
        insert_side_of_pear_deterioration_query += ', '.join(insert_side_of_pear_deterioration_query_values)
        self.db.execute(insert_side_of_pear_deterioration_query, insert_or_create_flg=True)

    def get_all(self) -> List[PearDb]:
        get_query = """
            SELECT 
                pears.pear_id,
                pr.rank_name,
                pears.created_at,
                pears.updated_at
            FROM pears
            INNER JOIN pear_ranks pr
            ON pr.pear_rank_id = pears.pear_rank_id
        """
        rows = self.db.execute(get_query)
        pears = []
        for row in rows:
            pear = PearDb(
                pear_id=row[0],
                rank_name=row[1],
                area_of_side=0.0,
                created_at="{0:%Y-%m-%d %H:%M}".format(row[2]),
                updated_at=row[3]
            )
            pears.append(pear)
        return pears


