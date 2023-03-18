import logging

from aiogram import Bot, types , Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook

API_TOKEN = '6228327366:AAFYQXCoM_D7wH860bTmKU4E4kdX-SG9K-w'

# webhook settings
WEBHOOK_HOST = 'https://fa77-178-155-28-88.eu.ngrok.io'
WEBHOOK_PATH = ''
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '127.0.0.1'  # or ip
WEBAPP_PORT = 80

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'])
async def echo(message: types.Message):
   return SendMessage(message.chat.id, message.text)

@dp.message_handler(commands=['help'])
async def echo(message: types.Message):
   return SendMessage(message.chat.id, 'Вы обратились к справке бота')

@dp.message_handler()
async def echo(message: types.Message):
   return SendMessage(message.chat.id, message.text)

async def on_startup(dp):
   await bot.set_webhook(WEBHOOK_URL)
   # insert code here to run it after start


async def on_shutdown(dp):
   logging.warning('Shutting down..')

   # insert code here to run it before shutdown

   # Remove webhook (not acceptable in some cases)
   await bot.delete_webhook()

   # Close DB connection (if used)
   await dp.storage.close()
   await dp.storage.wait_closed()

   logging.warning('Bye!')


if __name__ == '__main__':
   start_webhook(
       dispatcher=dp,
       webhook_path=WEBHOOK_PATH,
       on_startup=on_startup,
       on_shutdown=on_shutdown,
       skip_updates=True,
       host=WEBAPP_HOST,
       port=WEBAPP_PORT,
   )
