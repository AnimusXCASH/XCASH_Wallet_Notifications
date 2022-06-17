from tools.pushNotifierPager import PhonePushPager
from tools.discordPager import DiscordPager

class NotifiersManager:
    def __init__(self, settings:dict) -> None:
        self.phone = PhonePushPager(notifier_settings=settings["pushNotifier"])
        self.discord = DiscordPager(settings=settings["discord"])