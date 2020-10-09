import configparser
import os
import sys
parent_dir = os.path.dirname(sys.path[0])
sys.path.insert(0, parent_dir)
from database import *
from lib.logwriter import *
from lib.iniparser import *
import pandas as pd

class ConnDB_base:
    def __init__(self, url):
        self.db_agent = Database_connection(url)
        logger.debug("Database: init db success")

    def insertFrame(self, df, tablename):
        # try:
        df.to_sql(tablename, con=self.db_agent.engine,if_exists='append')
        logger.debug("Database: insertFrame success")
        # except:
        #     logger.error("Database: insertFrame error")

    def showTable(self, sql):
        # sql = "SELECT * FROM TEST"
        df = pd.read_sql(sql, con=self.db_agent.engine)
        return df

# if __name__ == '__main__':
#     db = ConnDB_base(db_url)
#     db.showTable()

