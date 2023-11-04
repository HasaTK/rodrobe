import requests

from typing import Optional
from src import config
from abc import ABC, abstractmethod

from src.exceptions import InvalidWebhookException


class AbstractWebhook(ABC):
    # TODO: Add more platforms

    @abstractmethod
    def send(self, content: str):
        pass

    @abstractmethod
    def raw_send(self, content):
        pass


class DiscordWebhook(AbstractWebhook):
    def __init__(
            self,
            webhook_url: Optional[str] = config.cfg_file["discord"]["sales_webhook"]
    ):
        self.webhook_url = webhook_url

    def send(self, content: str):

        """
        Posts the specified content through the webhook 

        :param str content:
        :return: request object 
        """

        newMsg = requests.post(
            self.webhook_url,
            json={"content": content}
        )

        if newMsg.status_code in (404, 401):
            raise InvalidWebhookException("The webhook URL provided was invalid")

        return newMsg

    def raw_send(self, content):

        """
        Posts raw content through the specified  webhook 

        :param  content:
        :return: request object 
        """

        newMsg = requests.post(
            self.webhook_url,
            json=content
        )

        if newMsg.status_code in (404, 401):
            raise InvalidWebhookException("The webhook URL provided was invalid")

        return newMsg
