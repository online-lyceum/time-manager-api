import asyncio
import logging
import types

from aiogram import Dispatcher, Bot
from fastapi import FastAPI, HTTPException

from time_manager import api
from time_manager import bot as bot_module


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] [%(process)s] [%(levelname)s] "
           "(%(filename)s:%(lineno)d) %(msg)s"
)
logger = logging.getLogger(__name__)
logger.info('Logger start work')



def init_telegram_pulling(
        application: FastAPI
):
    logger.info('Init telegram pulling')

    @application.on_event("startup")
    def on_startup():
        asyncio.create_task(bot_module.dp.start_polling())

    @application.on_event("shutdown")
    def on_shutdown():
        asyncio.create_task(bot_module.dp.stop_polling())


def init_telegram(
        application: FastAPI,
        config: 'Config()'
):
    bot, dp = bot_module.create_bot(config.telegram_token)
    url = config.dict(include={"telegram_webhook_url", "telegram_webhook_path"})
    logger.info(f'Start with {url}')
    if config.telegram_webhook_path == '' and config.telegram_webhook_url == '':
        init_telegram_pulling(application)
        return
    init_telegram_webhooks(
        application, bot, dp, config
    )


def init_telegram_webhooks(
        application: FastAPI,
        bot: Bot,
        dp: Dispatcher,
        config: 'Config()'
):
    logger.info('Init telegram webhooks')

    webhook_path = config.telegram_webhook_path

    if not config.telegram_webhook_path.startswith('/'):
        webhook_path = '/' + webhook_path
    if not config.telegram_webhook_path.endswith('/'):
        webhook_path = webhook_path + '/'

    webhook_url = (
            'https://'
            + config.telegram_webhook_url
            + webhook_path
            + config.telegram_token
    )

    @application.on_event("startup")
    async def on_startup():
        webhook_info = await bot.get_webhook_info()
        if webhook_info.url != webhook_url:
            await bot.set_webhook(
                url=webhook_url
            )

    @application.post(webhook_path + "{telegram_token}",
                      tags=['Telegram Webhooks'])
    async def bot_webhook(telegram_token: str, update: dict):
        if telegram_token != config.telegram_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        telegram_update = types.Update(**update)
        Dispatcher.set_current(dp)
        Bot.set_current(bot)
        await dp.process_update(telegram_update)

    @application.on_event("shutdown")
    async def on_shutdown():
        session = await bot.get_session()
        await session.close()
        asynciu.create_task(stop_notifications_cycle())


def create_application():
    application = FastAPI(
        openapi_url='/api/openapi.json',
        docs_url='/api/docs',
        redoc_url='/api/redoc',
        logger=logger
    )
    application.include_router(api.hello.router)
    application.include_router(api.user.router)
    application.include_router(api.note.router)
    application.include_router(api.auth.router)
    return application


app = create_application()
