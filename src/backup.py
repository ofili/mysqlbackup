import os
import subprocess
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SQL_FILE_EXTENSION = ".sql"


class MySQLBackupTool:
    def __init__(self, database_name, backup_dir, database_connector):
        self.database_name = database_name
        self.backup_dir = backup_dir
        self.database_connector = database_connector

    def create_backup(self):
        """
        Creates a backup of the MySQL database.

        :return:
            True if the backup was successful, False otherwise.
        """
        try:
            self.database_connector.connect()

            # Ensure the backup directory exists
            if not os.path.exists(self.backup_dir):
                os.makedirs(self.backup_dir)

            # Construct the file path with the current date
            current_date = datetime.now().strftime("%Y%m%d%H%M%S")
            backup_file_path = os.path.join(
                self.backup_dir,
                f"{self.database_name}_{current_date}{SQL_FILE_EXTENSION}",
            )

            # Use subprocess to execute mysqldump command
            with open(backup_file_path, "w") as backup_file:
                subprocess.run(
                    [
                        "mysqldump",
                        "-h",
                        "localhost",
                        "-u",
                        self.database_connector.username,
                        "-p",  # + self.database_connector.password,
                        self.database_name,
                    ],
                    stdout=backup_file,
                    text=True,
                    check=True,  # check=True to raise an exception for non-zero exit codes
                )

            logger.info("MySQL backup created successfully at: %s", backup_file_path)
            return True
        except subprocess.CalledProcessError as e:
            logger.error("Failed to create MySQL backup: %s", e)
            return False
        except Exception as e:
            logger.error("An unexpected error occurred: %s", e)
            return False
        finally:
            self.database_connector.disconnect()

    def verify_backup(self):
        """
        Verifies that the backup file is valid.

        :return:
            True if the backup file is valid, False otherwise.
        """
        backup_file = os.path.join(
            self.backup_dir, self.database_name + SQL_FILE_EXTENSION
        )

        if not os.path.exists(backup_file):
            return False

        try:
            self.database_connector.connect()
            with open(backup_file, "r") as f:
                first_line = f.readline()

                if not first_line.startswith("/*!40101 SET"):
                    return False

                f.read()
        except Exception as e:
            logger.error("Failed to verify MySQL backup: %s", e)
            return False
        finally:
            self.database_connector.disconnect()

        return True
