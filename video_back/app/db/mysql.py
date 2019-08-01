from app.config import Config
import easyapi

mysql_db = easyapi.MysqlDB(Config.MYSQL_USER, Config.MYSQL_PASSWORD, Config.MYSQL_HOST, Config.MYSQL_PORT,
                           Config.MYSQL_DATABASE)

mysql_db.connect()
