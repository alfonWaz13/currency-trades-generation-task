from dotenv import load_dotenv
import os

load_dotenv()


class MySqlConfig:
    HOST = os.getenv("MYSQL_HOST", "localhost")
    USER = os.getenv("MYSQL_USER", "ebury_user")
    PASSWORD = os.getenv("MYSQL_PASSWORD", "ebury_password")
    DATABASE = os.getenv("MYSQL_DATABASE", "ebury_prueba_tecnica")
    PORT = int(os.getenv("MYSQL_PORT", 3306))

    @classmethod
    def to_dict(cls):
        return {
            "host": cls.HOST,
            "user": cls.USER,
            "password": cls.PASSWORD,
            "database": cls.DATABASE,
            "port": cls.PORT
        }
