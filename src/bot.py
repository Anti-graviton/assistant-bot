# -*- coding: utf-8 -*-
import sys
import logging
from settings import settings
from mmpy_bot.bot import Bot, MattermostClient, PluginsManager, MessageDispatcher


logging.basicConfig(**{
    'format': '[%(asctime)s] %(message)s',
    'datefmt': '%m/%d/%Y %H:%M:%S',
    'level': logging.DEBUG if settings.DEBUG else logging.INFO,
    'stream': sys.stdout,
})


class AssistantBot(Bot):
    def __init__(self):
        self._client = MattermostClient(
            settings.BOT_URL, settings.BOT_TEAM,
            settings.BOT_LOGIN, settings.BOT_PASSWORD,
            settings.SSL_VERIFY
        )
        self._plugins = PluginsManager()
        self._plugins.init_plugins()
        self._dispatcher = MessageDispatcher(self._client, self._plugins)


if __name__ == "__main__":
    AssistantBot().run()

