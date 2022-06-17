import requests
import requests.exceptions
from http.client import HTTPException
import urllib3.exceptions
import socket


class DiscordPager:
    def __init__(self, settings):
        self.active = settings["active"]
        self.deposit_channel = settings["deposits"]

    def deposit_processed(self, text):
        """
        Push notification to Discord to monitor deposits
        :param text: Data on the deposit
        :return:
        """
        if self.active:
            embed = {
                "description": "New Deposit To Wallet",
                "title": f"New deposit to your wallet has been processed",
                "color": 3066993,
                "fields": [
                    {"name": "Details",
                     "value": text}
                ]
            }

            data = {
                "username": "Wallet Monitor",
                "embeds": [
                    embed
                ],
            }
            try:
                requests.post(self.deposit_channel, json=data)
            except (requests.exceptions.ConnectionError, urllib3.exceptions.ProtocolError, HTTPException, socket.error,
                    urllib3.exceptions.ReadTimeoutError, requests.exceptions.ReadTimeout) as e:
                print(f"Discord webhook error: {e}")

    def balance_status(self, text):
        """
        Push notification to Discord balances
        :param text: Data on the deposit
        :return:
        """
        if self.active:
            embed = {
                "description": "Wallet balance status after processing...",
                "title": f"New Wallet Balance Information",
                "color": 3066993,
                "fields": [
                    {"name": "Wallet Balance",
                     "value": text}
                ]
            }

            data = {
                "username": "Wallet Monitor",
                "embeds": [
                    embed
                ],
            }
            try:
                requests.post(self.deposit_channel, json=data)
            except (requests.exceptions.ConnectionError, urllib3.exceptions.ProtocolError, HTTPException, socket.error,
                    urllib3.exceptions.ReadTimeoutError, requests.exceptions.ReadTimeout) as e:
                print(f"Discord webhook error: {e}")

    def exception_found(self, text):
        if self.active:
            embed = {
                "description": "Exception on System",
                "title": f"Some issue :think:",
                "color": 3066993,
                "fields": [
                    {"name": "Details",
                     "value": text}
                ]
            }

            data = {
                "username": "Exception issue Monitor",
                "embeds": [
                    embed
                ],
            }
            try:
                requests.post(self.deposit_channel, json=data)
            except (requests.exceptions.ConnectionError, urllib3.exceptions.ProtocolError, HTTPException, socket.error,
                    urllib3.exceptions.ReadTimeoutError, requests.exceptions.ReadTimeout) as e:
                print(f"Discord webhook error: {e}")
