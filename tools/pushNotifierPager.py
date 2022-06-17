from pushnotifier import PushNotifier as pn
import requests
import urllib3
import requests.exceptions
from http.client import HTTPException
import socket


class PhonePushPager:
    def __init__(self, notifier_settings:dict):
        self.username = notifier_settings["username"]
        self.password = notifier_settings["password"]
        self.app_name = notifier_settings["appName"]
        self.token = notifier_settings["token"]
        self.activated = notifier_settings["active"]
        self.cleint = None

        # Check if is activated in settings script
        if self.activated:
            self.client = pn.PushNotifier(self.username, self.password, self.app_name, self.token)
    


    def phone_ping(self, text):
        """Send the ping message to phone

        Args:
            text (str): Message you would like to send to phone
        """
        if self.activated:
            try:
                self.client.send_text(text)
            except (requests.exceptions.ConnectionError, urllib3.exceptions.ProtocolError, HTTPException, socket.error,
                    urllib3.exceptions.ReadTimeoutError, requests.exceptions.ReadTimeout) as e:
                print(f"Could not push to phone: {e}")
