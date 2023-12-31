import argparse
import json
import logging
import os
import schedule
import time

from src.connector import DatabaseConnector
from src.manager import MySQLBackupManager
from src.notification import NotificationSender
from src.core.config import get_settings, Settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SCHEDULE_FILE = "backup_schedule.json"


class DatabaseConnectorEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, DatabaseConnector):
            return {
                "host": obj.host,
                "port": obj.port,
                "username": obj.username,
                "password": obj.password,
                "database": obj.database,
            }
        return super().default(obj)


def configure_logging():
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def backup_job(database_connector, backup_dir):
    try:
        notification_sender = NotificationSender()
        backup_manager = MySQLBackupManager(
            database_name=database_connector.database,
            backup_dir=backup_dir,
            notification_sender=notification_sender,
            database_connector=database_connector,
        )

        success = backup_manager.backup()

        if not success:
            logger.error("Backup job failed. Check logs for details.")
            # Add code for sending error notifications if needed
            return

        backup_manager.verify()

    except Exception as e:
        logger.error(f"An unexpected error occurred during backup job: {e}")


def load_schedule() -> dict:
    if os.path.exists(SCHEDULE_FILE) and os.path.getsize(SCHEDULE_FILE) > 0:
        with open(SCHEDULE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_schedule():
    job_data = []

    for job in schedule.get_jobs():
        job_data.append(
            {
                "job_func": job.job_func.__name__,
                "args": job.job_func.args,
                "kwargs": job.job_func.keywords,
                "at_time": str(job.at_time),
            }
        )

    with open(SCHEDULE_FILE, "w") as f:
        json.dump(job_data, f, cls=DatabaseConnectorEncoder)


def main(argv=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--database", dest="database", help="Name of the database to backup."
    )
    parser.add_argument("--dir", dest="dir", help="Backup destination directory.")

    known_args, _ = parser.parse_known_args(argv)

    configure_logging()

    setting: Settings = get_settings()

    database_connector = DatabaseConnector(
        host=setting.host,
        port=int(setting.port),
        username=setting.user,
        password=setting.password,
        database=known_args.database,
    )

    # Run the backup job immediately
    backup_job(database_connector, known_args.dir)

    # Load existing schedule
    existing_schedule = load_schedule()
    for job_data in existing_schedule:
        schedule.every().day.at(job_data["at_time"]).do(
            backup_job, database_connector, known_args.dir
        )

    # Schedule the backup to run daily at a specific time (e.g., 2:00 AM)
    schedule.every().day.at("02:00").do(backup_job, database_connector, known_args.dir)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
            save_schedule()  # Save the schedule to the file
    except KeyboardInterrupt:
        logger.info("Script interrupted by user.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
