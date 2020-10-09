import configparser
import os
import sys
parent_dir = os.path.dirname(sys.path[0])
sys.path.insert(0, parent_dir)
import psycopg2

config = configparser.ConfigParser()
config.read('doc/settings.ini')

db_url = 'mysql://{}:{}@localhost:{}/{}?charset=utf8'.format(config["database"]["user"], config["database"]["password"], 
            config["database"]["port"], config["database"]["database"])
db_weather = 'mysql://{}:{}@localhost:{}/{}?charset=utf8'.format(config["database_weather"]["user"], config["database_weather"]["password"], 
            config["database_weather"]["port"], config["database_weather"]["database"])






