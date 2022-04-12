from datetime import datetime, timedelta, timezone
from src.utils.db_connector import DbConnector

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class AbstractRepository:
    def __init__(self):
        self.db = DbConnector()

    @staticmethod
    def get_now():
        jst = timezone(timedelta(hours=+9), 'JST')
        now = datetime.now(jst).strftime(DATE_FORMAT)
        return now
