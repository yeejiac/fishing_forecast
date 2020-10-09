from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.table import *

class Database_connection:
    def __init__(self, url):
        self.engine = create_engine(url, echo = True)
        self.session = sessionmaker(bind=self.engine)()

    # def __del__(self):
    #     self.session.close()