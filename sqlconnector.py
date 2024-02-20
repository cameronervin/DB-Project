import pandas as pd
from dotenv import load_dotenv
import pymysql
import os

load_dotenv()

class SqlQueryRunner:
    def __init__(self,suppress_output=False):
        _host = os.getenv("HOST")
        _user = os.getenv("DBUSERNAME")
        _pass = os.getenv("PASSWORD")
        db_name = os.getenv("DB_NAME")
        if not suppress_output:
            print(f"""CONNECTION USING:
                    hostname: {_host}
                    user: {_user}
                    password: {_pass}
                    db_name: {db_name}
                """)
        self._host = _host
        self._user = _user
        self._pass = _pass
        self.db_name = db_name
    
    def get_conn(self):
        return pymysql.connect(
            host=self._host,
            user=self._user,
            password=self._pass,
            db=self.db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
    
    def runSelect(self,query):
        rows = pd.DataFrame()
        try:
            conn = self.get_conn()
            with conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                rows = pd.DataFrame(rows)
            return rows
        except Exception as e:
            print(repr(e))
            return False
        finally:
            conn.close()

    def runChanger(self,query):
        try:
            conn = self.get_conn()
            with conn.cursor() as cursor:
                cursor.execute(query)

            conn.commit()
            return True
        except Exception as e:
            print(repr(e))
            return False
        finally:
            conn.close()