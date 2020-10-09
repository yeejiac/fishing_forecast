from loguru import logger
import datetime
import os
import sys
parent_dir = os.path.dirname(sys.path[0])
sys.path.insert(0, parent_dir)
dt = datetime.datetime.now()
logger.add("../doc/log/{}.log".format(dt.strftime('%Y-%d-%m')), format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")

# logger.debug("test")
