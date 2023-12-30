# database_connector.py
import pymysql
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class DatabaseConnector:
    def __init__(self, host, port, username, password, database):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host, port=self.port, user=self.username, password=self.password, db=self.database
            )
            logger.info("Connected successfully")
        except pymysql.Error as e:
            logger.error("Failed to connect to the database: %s", e)

    def disconnect(self):
        if self.connection is not None:
            try:
                self.connection.close()
                logger.info("Disconnected successfully")
            except pymysql.Error as e:
                logger.error("Failed to disconnect from the database: %s", e)
