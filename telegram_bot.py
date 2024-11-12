import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import aioschedule

from parser import *

# чтение файла с балансом
f = open('balance.txt', 'r')
for line in f:
	balance = f 


bot = Bot(token='7258056588:AAG3ir0fH5csuPjJPVLnbNjFeXs1aFDBH9Y')

dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
	await message.answer('Hello user')

async def get_message():
	await bot.send_message(balance)
	await aioschedule.run_pending()
	await asyncio.sleep(1)



async def main():
	await dp.start_polling(bot)


if __name__ == '__main__':
	asyncio.run(main())