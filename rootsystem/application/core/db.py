import MySQLdb
from settings import DB_HOST, DB_USER, DB_PASS, DB_NAME


class DBQuery(object):

    def execute(self, sql):
        self.sql = sql
        datos = [DB_HOST, DB_USER, DB_PASS, DB_NAME]
        conn = MySQLdb.connect(*datos)
        cursor = conn.cursor()
        cursor.execute(self.sql)
        data = True

        if self.limpiar_sql().upper().startswith('SELECT'):
            data = cursor.fetchall()
        else:
            conn.commit()
            if self.limpiar_sql().upper().startswith('INSERT'):
                data = cursor.lastrowid

        cursor.close()
        conn.close()
        return data

    def limpiar_sql(self):
        return self.sql.replace(' ', '').replace('\n', '')
