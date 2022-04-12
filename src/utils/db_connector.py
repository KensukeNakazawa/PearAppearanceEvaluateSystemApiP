import os
import MySQLdb


class DbConnector:

    def __init__(self) -> None:
        self.conn = MySQLdb.connect(
            user=os.environ['DB_USERNAME'],
            passwd=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST'],
            db=os.environ['DB_DATABASE'],
            use_unicode=True,
            charset='utf8'
        )
        self.cursor = self.conn.cursor()

    def execute(self, sql: str, insert_or_create_flg: bool = False) -> tuple:
        """入力したクエリを実行する
        Args:
            sql(str): 実行するクエリ
            insert_or_create_flg(bool): 作成するかどうか
        Returns:
            rows(tuple): SQLにより、取得したデータ
        """
        row = self.cursor.execute(sql)
        if insert_or_create_flg:
            self.conn.commit()
        else:
            row = self.cursor.fetchall()
        return row

    def transaction(self):
        self.cursor.execute('START TRANSACTION;')

    def rollback(self):
        self.cursor.execute('ROLLBACK;')

    def commit(self):
        self.cursor.execute('COMMIT;')
