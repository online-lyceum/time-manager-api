from time_manager.bot import create_bot
import asyncio
from os import environ


if __name__ == '__main__':
    dp, bot = create_bot(environ['BOT_TOKEN'])
    print(dp)
    asyncio.run(dp.start_polling())