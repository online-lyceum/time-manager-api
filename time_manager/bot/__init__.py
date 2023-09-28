from aiogram import Dispatcher, Bot


bot: Bot | None = None
dp: Dispatcher | None = None


def create_bot(token: str) -> 'Bot, Dispatcher':
    global bot, dp
    bot = Bot(token=token)
    dp = Dispatcher(bot)

    from . import note

    return bot, dp