import pymysql.cursors
import os
from dotenv import load_dotenv

load_dotenv()

class MySQLConnection:
    def __init__(self, db):
        connection = pymysql.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", "root"),
            db=db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        self.connection = connection

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                cursor.execute(query)
                clean_query = query.strip().lower()

                if clean_query.startswith("insert"):
                    return cursor.lastrowid
                elif clean_query.startswith("select"):
                    return cursor.fetchall()
                else:
                    return True
            except Exception as e:
                print("Error en consulta MySQL:", e)
                if query.strip().lower().startswith("select"):
                    return []
                return False

def connectToMySQL(db):
    return MySQLConnection(db)