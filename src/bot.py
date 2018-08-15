from mmpy_bot.bot import Bot, MattermostClientv4, PluginsManager, MessageDispatcher
from settings import settings

class AssistantBot(Bot):
    def __init__(self):
        self._client = MattermostClientv4(
            settings.BOT_URL, settings.BOT_TEAM,
            settings.BOT_LOGIN, settings.BOT_PASSWORD,
            settings.SSL_VERIFY
        )
        self._plugins = PluginsManager()
        self._plugins.init_plugins()
        self._dispatcher = MessageDispatcher(self._client, self._plugins)

if __name__ == "__main__":    
    AssistantBot().run()