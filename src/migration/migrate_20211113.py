import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from dotenv import load_dotenv

from utils.db_connector import DbConnector


def main():
    db = DbConnector()

    queries = []

    drop_evaluate_flg_from_pears_table = """
        ALTER TABLE pears
        DROP evaluate_flg;
    """
    queries.append(drop_evaluate_flg_from_pears_table)

    create_pear_ranks_table = """
        CREATE TABLE IF NOT EXISTS pear_ranks (
            pear_rank_id BIGINT NOT NULL AUTO_INCREMENT UNIQUE COMMENT '主キー',
            rank_name VARCHAR(256) NOT NULL COMMENT '等級の名前',
            PRIMARY KEY (pear_rank_id)
        );
    """
    queries.append(create_pear_ranks_table)

    insert_initial_data_for_pear_ranks_table_query = """
        INSERT INTO pear_ranks 
            (rank_name)
        VALUES
            ('Not_Yet'),
            ('No'),
            ('Good'),
            ('Blue'),
            ('Red')
    """
    queries.append(insert_initial_data_for_pear_ranks_table_query)

    add_pear_rank_id_to_pears_table = """
        ALTER TABLE pears
        ADD (
            pear_rank_id BIGINT NOT NULL DEFAULT 1 COMMENT '外部キー(pear_ranks.pear_rank_id)',
            FOREIGN KEY (pear_rank_id) REFERENCES pear_ranks (pear_rank_id)
        );
    """
    queries.append(add_pear_rank_id_to_pears_table)

    for query in queries:
        db.execute(query, insert_or_create_flg=True)


if __name__ == '__main__':
    load_dotenv()
    main()