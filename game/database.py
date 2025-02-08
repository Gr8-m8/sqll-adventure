import sqlite3
try:
    import mariadb
    OFFLINE = False
except ModuleNotFoundError:
    OFFLINE = True

from connection import ServerConnection
import usysf

class ManagerDB:
    STATUS = False
    """db communication"""
    def __init__(self, connection: ServerConnection):
        STATUS = False

    def close(self):
        """close db connection"""
        return None

    def raw(self, cmd, debug=False) -> str:
        """raw sql cmd"""
        return cmd

    def create_table(self, table: str, schema: str, debug: bool = False) -> str:
        """table into db"""
        cmd = f"CREATE TABLE IF NOT EXISTS {table} ({schema});"
        return cmd

    def save(self) -> None:
        """save db"""
        return None

    def insert(self, table: str, datav: list, debug: bool = False) -> str:
        """data into db"""
        data = ', '.join(datav)

        cmd = f"INSERT INTO {table} VALUES ({data});"
        return cmd

    def update(self, table: str, datakv: dict, identifierkv: dict, debug: bool = False) -> str:
        """change data in db"""
        data = ', '.join(f"{k}={v}" for k, v in datakv.items())
        data.replace(':', '=')

        identifier = ' AND '.join(f"{k}={v}" for k, v in identifierkv.items())
        identifier.replace(':', '=')

        cmd = f"UPDATE {table} SET {data} WHERE {(identifier)};"
        return cmd

    def select(self, table: str, datak: list, identifierkv: dict = None, debug: bool = False) -> str:
        """get data in db"""
        data = ', '.join(datak)
        if identifierkv:
            identifier = ' AND '.join(f"{k}={v}" for k, v in identifierkv.items())
            identifier.replace(':', '=')
        else:
            identifier = None

        fs1 = f"SELECT {data} FROM {table} WHERE {(identifier)}"
        fs2 = f"SELECT {data} FROM {table}"
        cmd = fs1 if identifier else fs2
        return cmd

    def delete(self, table: str, identifierkv: dict, debug: bool = False) -> str:
        """remove data in db"""
        identifier = ' AND '.join(f"{k}={v}" for k, v in identifierkv.items())
        identifier.replace(':', '=')

        cmd = f"DELETE FROM {table} WHERE identifier"
        return cmd

    def table_len(self, table: str) -> int:
        """len of table in db"""
        ret = 0
        get = self.select(table, ['count(*)'])
        if get:
            ret = get
        return get if get else ret

class MariaDB(ManagerDB):
    """Mariadb db communication"""

    def __init__(self, connection: ServerConnection):
        self.db = None
        self.cursor = None
        try:
            self.db = mariadb.connect(
                user=str(connection.DB_GAME_USER),
                password=str(connection.DB_GAME_USER_PWD),
                host=str(connection.DB_IP),
                port=int(str(connection.DB_PORT)),
                database=str(connection.DB_FILE)
            )
            self.cursor = self.db.cursor()
            self.db.autocommit = False
            super().__init__(connection)
            ManagerDB.STATUS = True
        except mariadb.Error as e:
            ManagerDB.STATUS = False
            usysf.log(f"MARIADB ERROR: {e}")
            input("CONFIRM")
            #exit(1)

    def close(self):
        self.db.close()
        return super().close()

    def raw(self, cmd, debug=False):
        """raw sql cmd"""
        cmd = super().raw(cmd)
        val = self.cursor.execute(cmd) if not debug else cmd
        try:
            return self.cursor.fetchall()
        except:
            return []

    def create_table(self, table: str, schema: str, debug: bool = False) -> list:
        """table into db"""
        cmd = f"CREATE TABLE IF NOT EXISTS {table} ({schema});"
        val = self.cursor.execute(cmd) if not debug else cmd
        try:
            return self.cursor.fetchall()
        except:
            return []

    def save(self) -> None:
        """save db"""
        return self.db.commit()

    def insert(self, table: str, datav: list, debug: bool = False) -> list:
        """data into db"""
        cmd = super().insert(table, datav, debug)
        val = self.cursor.execute(cmd) if not debug else cmd
        return

    def update(self, table: str, datakv: list, identifierkv: dict, debug: bool = False) -> list:
        """change data in db"""
        cmd = super().update(table, datakv, identifierkv, debug)
        val= self.cursor.execute(cmd) if not debug else cmd
        try:
            return self.cursor.fetchall()
        except:
            return []

    def select(self, table: str, datak: list, identifierkv: dict = None, debug: bool = False) -> list:
        """get data in db"""
        cmd = super().select(table, datak, identifierkv, debug)
        val = self.cursor.execute(cmd) if not debug else cmd
        try:
            return self.cursor.fetchall()
        except:
            return []

    def delete(self, table: str, identifierkv: dict, debug: bool = False) -> list:
        """remove data in db"""
        cmd = super().delete(table, identifierkv, debug)
        val= self.cursor.execute(cmd) if not debug else cmd
        try:
            return self.cursor.fetchall()
        except:
            return []

    def table_len(self, table: str) -> int:
        """len of table in db"""
        val = self.select(table, ['count(*)'])
        val = val[0][0]
        try:
            return val
        except:
            return 0

class Sqllite3DB(ManagerDB):
    """sqlite3 db communication"""

    def __init__(self, connection: ServerConnection):
        self.db = sqlite3.connect(connection.DB_FILE)
        self.cursor = self.db.cursor()
        super().__init__(connection)
        ManagerDB.STATUS = True

    def close(self):
        return super().close()

    def raw(self, cmd, debug=False):
        """raw sql cmd"""
        cmd = super().raw(cmd)
        return self.cursor.execute(cmd).fetchall() if not debug else cmd

    def create_table(self, table: str, schema: str, debug: bool = False) -> list:
        """table into db"""
        cmd = f"CREATE TABLE IF NOT EXISTS {table} ({schema});"
        return self.cursor.execute(cmd) if not debug else cmd

    def save(self) -> None:
        """save db"""
        return self.db.commit()

    def insert(self, table: str, datav: list, debug: bool = False) -> list:
        """data into db"""
        cmd = super().insert(table, datav, debug)
        return self.cursor.execute(cmd).fetchall() if not debug else cmd

    def update(self, table: str, datakv: list, identifierkv: dict, debug: bool = False) -> list:
        """change data in db"""
        cmd = super().update(table, datakv, identifierkv, debug)
        return self.cursor.execute(cmd).fetchall() if not debug else cmd

    def select(self, table: str, datak: list, identifierkv: dict = None, debug: bool = False) -> list:
        """get data in db"""
        cmd = super().select(table, datak, identifierkv, debug)
        return self.cursor.execute(cmd).fetchall() if not debug else cmd

    def delete(self, table: str, identifierkv: dict, debug: bool = False) -> list:
        """remove data in db"""
        cmd = super().delete(table, identifierkv, debug)
        return self.cursor.execute(cmd).fetchall() if not debug else cmd

    def table_len(self, table: str) -> int:
        """len of table in db"""
        ret = self.select(table, ['count(*)'])
        return int(ret[0][0])