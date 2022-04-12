import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from dotenv import load_dotenv

from utils.db_connector import DbConnector


def main():
    db = DbConnector()

    queries = []

    create_pears_table = """
        CREATE TABLE IF NOT EXISTS pears (
            pear_id BIGINT NOT NULL AUTO_INCREMENT UNIQUE COMMENT '主キー',
            evaluate_flg TINYINT(1) NOT NULL DEFAULT 0 COMMENT '評価済みかどうかのフラグ',
            area_of_side DOUBLE DEFAULT 0 COMMENT '側面の合計ピクセル',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
            PRIMARY KEY (pear_id)
        );
    """
    queries.append(create_pears_table)

    create_side_of_pears_table = """
        CREATE TABLE IF NOT EXISTS side_of_pears (
            side_of_pear_id BIGINT NOT NULL AUTO_INCREMENT UNIQUE COMMENT '主キー',
            pear_id BIGINT NOT NULL COMMENT '外部キー(pears.pear_id)',
            image_path VARCHAR(256) NOT NULL COMMENT '画像を保存しているフルパス',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
            PRIMARY KEY (side_of_pear_id),
            FOREIGN KEY (pear_id) REFERENCES pears (pear_id)
        );
    """
    queries.append(create_side_of_pears_table)

    create_evaluated_side_of_pears_table = """
        CREATE TABLE IF NOT EXISTS evaluated_side_of_pears (
            evaluated_side_of_pear_id BIGINT NOT NULL AUTO_INCREMENT UNIQUE COMMENT '主キー',
            pear_id BIGINT NOT NULL COMMENT '外部キー(pears.pear_id)',
            image_path VARCHAR(256) NOT NULL COMMENT '画像を保存しているフルパス',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
            PRIMARY KEY (evaluated_side_of_pear_id),
            FOREIGN KEY (pear_id) REFERENCES pears (pear_id)
        );
    """
    queries.append(create_evaluated_side_of_pears_table)

    create_pear_deteriorations_table = """
        CREATE TABLE IF NOT EXISTS pear_deteriorations (
            pear_deterioration_id BIGINT NOT NULL AUTO_INCREMENT UNIQUE COMMENT '主キー',
            code VARCHAR(256) NOT NULL COMMENT '外観汚損のコード',
            deterioration_name VARCHAR(256) NOT NULL COMMENT '外観汚損の名前',
            color_b TINYINT UNSIGNED NOT NULL COMMENT '外観汚損につける色コード(B)',
            color_g TINYINT UNSIGNED NOT NULL COMMENT '外観汚損につける色コード(G)',
            color_r TINYINT UNSIGNED NOT NULL COMMENT '外観汚損につける色コード(R)',
            PRIMARY KEY (pear_deterioration_id)
        );
    """
    queries.append(create_pear_deteriorations_table)

    create_side_of_pear_deteriorations_table = """
        CREATE TABLE IF NOT EXISTS side_of_pear_deteriorations (
            side_of_pear_deterioration_id BIGINT NOT NULL AUTO_INCREMENT UNIQUE COMMENT '主キー',
            evaluated_side_of_pear_id BIGINT NOT NULL COMMENT '外部キー(evaluated_side_of_pears.evaluated_side_of_pear_id)',
            pear_deterioration_id BIGINT NOT NULL COMMENT '外部キー(pear_deteriorations.pear_deterioration_id)',
            top_y INT NOT NULL COMMENT '画像中の左上のy座標',
            left_x INT NOT NULL COMMENT '画像中の左上のx座標',
            under_y INT NOT NULL COMMENT '画像中の右下のy座標',
            right_x INT NOT NULL COMMENT '画像中の右下のx座標',
            ratio DOUBLE NOT NULL COMMENT '画像中の当該汚損の比率',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
            PRIMARY KEY (side_of_pear_deterioration_id),
            FOREIGN KEY (evaluated_side_of_pear_id) REFERENCES evaluated_side_of_pears (evaluated_side_of_pear_id),
            FOREIGN KEY (pear_deterioration_id) REFERENCES pear_deteriorations (pear_deterioration_id)
        );
    """
    queries.append(create_side_of_pear_deteriorations_table)

    insert_initial_data_for_pear_deteriorations_table_query = """
        INSERT INTO pear_deteriorations 
            (code, deterioration_name, color_b, color_g, color_r)
        VALUES
            ('AN', 'alternalia', 255, 255, 0),
            ('IJ', 'injury', 214, 112, 218),
            ('SK', 'speckle', 133, 21, 199),
            ('PN', 'plane', 0, 0, 255),
            ('CM', 'chemical', 71, 99, 255)
    """
    queries.append(insert_initial_data_for_pear_deteriorations_table_query)

    for query in queries:
        db.execute(query, insert_or_create_flg=True)


if __name__ == '__main__':
    load_dotenv()
    main()
