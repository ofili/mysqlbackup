from src.backup import MySQLBackupTool


class MySQLBackupManager:
    def __init__(self, database_name, backup_dir, notification_sender, database_connector):
        self.database_name = database_name
        self.backup_tool = MySQLBackupTool(database_name, backup_dir, database_connector)
        self.notification_sender = notification_sender

    def backup(self):
        """
        Creates a backup of the MySQL database and sends a notification to the admin if the backup is successful.
        """
        if self.backup_tool.create_backup():
            self.notification_sender.send_notification(f"MySQL backup for {self.database_name} created successfully.")
