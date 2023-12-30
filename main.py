# main.py
import argparse
from src.connector import DatabaseConnector

from src.manager import MySQLBackupManager
from src.notification import NotificationSender


def main(argv=None):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--host", dest="host", help="Database server address including port.")
    parser.add_argument("--port", dest="port", help="The server port address")
    parser.add_argument("--username", dest="username", help="Username with permission to perform backup.")
    parser.add_argument("--password", dest="password", help="Password for the user account.")
    parser.add_argument("--database", dest="database", help="Name of the database to backup.")
    parser.add_argument("--dir", dest="dir", help="Backup destination directory.")

    known_args, _ = parser.parse_known_args(argv)

    database_connector = DatabaseConnector(
        host=known_args.host,
        port=int(known_args.port),
        username=known_args.username,
        password=known_args.password,
        database=known_args.database
    )
    notification_sender = NotificationSender()
    backup_manager = MySQLBackupManager(
        database_name=known_args.database,
        backup_dir=known_args.dir,
        notification_sender=notification_sender,
        database_connector=database_connector
    )

    backup_manager.backup()


if __name__ == "__main__":
    main()
