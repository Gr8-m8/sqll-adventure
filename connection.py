class ServerConnection:
    """server connection"""
    def __init__(self):
        self.SERVER_HOST_PASSWORD="PASSWORD"
        self.DB_GAME_USER="game"
        self.DB_GAME_USER_PWD="game"
        self.DB_IP="127.0.0.1"
        self.DB_PORT="3306"
        self.DB_FILE="game.db"
        self.offline = True

    def get_data_txt(self) -> list:
        """connection data as str kv list"""
        return [
            f'SERVER_HOST_PASSWORD="{self.SERVER_HOST_PASSWORD}"',
            f'DB_GAME_USER="{self.DB_GAME_USER}"',
            f'DB_GAME_USER_PWD="{self.DB_GAME_USER_PWD}"',
            f'DB_IP="{self.DB_IP}"',
            f'DB_PORT="{self.DB_PORT}"',
            f'DB_FILE="{self.DB_FILE}"',
        ]
    
    def get_data(self) -> list:
        """connection data as v list"""
        return [
            self.SERVER_HOST_PASSWORD,
            self.DB_GAME_USER,
            self.DB_GAME_USER_PWD,
            self.DB_IP,
            self.DB_PORT,
            self.DB_FILE,
        ]

    def set_offline(self, val: bool):
        """set offline status"""
        self.offline = val

    def set_server_host_pw(self, val: str):
        """set db root pw"""
        self.SERVER_HOST_PASSWORD = val

    def set_ip(self, val: str):
        """set db ip"""
        self.DB_IP = val

    def set_port(self, val: str):
        """set db port"""
        self.DB_PORT = val

    def set_game_user(self, val: str):
        """set db service user"""
        self.DB_GAME_USER = val

    def set_game_user_pw(self, val: str):
        """set db service user pw"""
        self.DB_GAME_USER_PWD=val

    def set_db_file(self, val: str):
        """set db file"""
        self.DB_FILE=val

    def toENV(self, data: list = None):
        """values to .env for docker host"""
        try:
            open('.env', 'x', encoding='utf-8')
        except Exception as e:
            print(e)
        with open('.env', 'w', encoding='utf-8') as file:
            if not data:
                data = self.get_data_txt()
            for dataentry in data:
                file.write(dataentry+"\n")
            file.close()


    def toServerList(self, listname: str) -> list:
        """connection history"""
        try:
            open(f'data/{listname}_server.data', 'x', encoding='utf-8')
        except Exception as e:
            print(e)
        with open(f'data/{listname}_server.data', 'a', encoding='utf-8') as file:
            data = self.get_data_txt()
            file.write('|'.join(data)+"\n")
            file.close()
        return data