import psycopg2
#from datetime import datetime, timedelta
from configparser import ConfigParser
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def config(filename=BASE_DIR+'/database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def postgre_conn():
    params = config()
    conn = psycopg2.connect(**params)
    return conn

db_conn = postgre_conn()
cur = db_conn.cursor()
cur.execute('select * from "user"')
data = cur.fetchall()
for row in data:
    print(row[0])
