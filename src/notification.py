import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class NotificationSender:
    @staticmethod
    def send_notification(message):
        logger.info(message)
