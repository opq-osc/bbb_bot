import mysql.connector.pooling

from util.db.config import config_dict

db_pool = mysql.connector.pooling.MySQLConnectionPool(**config_dict, charset="utf8mb4", pool_name="pool", pool_size=32)
