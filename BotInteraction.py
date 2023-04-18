import logging
import DBInteraction
import json

from aiogram import Bot, Dispatcher, executor, types

Settings = ""

with open('Settings.json', 'r') as f: 
    text = f.read()
    Settings = json.loads(text)
    f.close()

API_TOKEN = Settings["BOT_TOKEN"]

logging.basicConfig(level=logging.INFO) 

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

''' type: 1 - find; 2 - add; 3 - update; 4 - delete '''
async def user_interactionin(type):
    
    bot = Bot.get_current()
    user = types.User.get_current()

    if type == 3 or type == 2:
        executionStatus = DBInteraction.bot_interactionin_db(type, user.id, Settings, user.full_name)
    else:
        executionStatus = DBInteraction.bot_interactionin_db(type, user.id, Settings)
    
    if executionStatus is None:
        return False
    else:
        return True      

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
 
    userFind = await user_interactionin(1)

    if userFind:
        await message.reply("Hi! username")    
    else:
        await message.reply("Hi!\nI'm ArtSoft UZ Bot!\nYou want to register?\nWrite command /registration")
    
@dp.message_handler(commands=['registration'])
async def send_welcome(message: types.Message):
 
    userAdd = await user_interactionin(2)

    if userAdd:
        await message.reply("You are registered")    
    else:
        await message.reply("You are already registered")

@dp.message_handler(commands=['update'])
async def send_welcome(message: types.Message):
 
    userAdd = await user_interactionin(3)

    if userAdd:
        await message.reply("You are update")    
    else:
        await message.reply("You are not update")

@dp.message_handler(commands=['delete'])
async def send_welcome(message: types.Message):
 
    userAdd = await user_interactionin(4)

    if userAdd:
        await message.reply("You are delete")    
    else:
        await message.reply("You are not delete")

@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)

if __name__ == '__main__':
    
    executor.start_polling(dp, skip_updates=True)