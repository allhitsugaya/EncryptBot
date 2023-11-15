import asyncio
import nacl ,nacl.utils,nacl.secret
import pycparser
from aiogram import Bot, Dispatcher, filters, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from nacl.public import PrivateKey, Box
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove,KeyboardButton
import config


bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot=bot)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
secret_key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
box = nacl.secret.SecretBox(secret_key)
button1 = KeyboardButton("Підтримка")
button2 = KeyboardButton("Список команд")
keyboard1  = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button1).add(button2)

class States(StatesGroup):
    INPUT_TEXT = State()
    DECRYPT_TEXT = State()
keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard1.add("Підтримка", "Список команд")
    

@dp.message_handler(filters.Command(commands=["start"]))
async def cmd_start(message: types.Message):
    await message.answer("Привіт, я Бот для шифрування повідомлення та їх дешифрування", reply_markup=keyboard1)

@dp.message_handler(filters.Command(commands=["help"]))
async def cmd_help(message: types.Message):
    await message.answer("Підтримка бота - @all_hitsugaya", reply_markup= keyboard1)

@dp.message_handler(filters.Command(commands=["mama"]))
async def cmd_mama(message: types.Message):
    await message.answer("I love my mom")

@dp.message_handler(filters.Command(commands=["info"]))
async def cmd_info(message: types.Message):
    await message.answer('''Інформація щодо цього бота:
Libraries:
aiogram~=2.25
pynacl~=1.5.0
pycparser~=2.21
Writer:
@all_hitsugaya''')

@dp.message_handler(filters.Command(commands=["encrypt"]))
async def cmd_encrypt(message: types.Message):
    await message.reply("Будь ласка, введіть текст для шифрування:", reply_markup= keyboard1)
    await States.INPUT_TEXT.set()

@dp.message_handler(filters.Command(commands=["decrypt"]))
async def cmd_decrypt(message: types.Message):
    await message.reply("Будь ласка, введіть текст для дешифрування:", reply_markup= keyboard1)
    await States.DECRYPT_TEXT.set()

@dp.message_handler(filters.Command(commands=["start"]))
async def kbanswer (message: types.Message):
      await message.reply("Ваше меню:" , reply_markup= keyboard1)
      
@dp.message_handler()
async def menu(message: types.Message):
  if message.text == "Підтримка" :
     await message.answer("Підтримка бота - @all_hitsugaya")
  elif message.text == "Список команд" :
      await message.answer(''' Список всіх доступних команд:
/encrypt - Шифрація повідомлень.
/decrypt - Дешифрація повідомлень.
/help - Підтримка.
/info - інформація щодо бота.''')
  else :
      await message.answer(f"Сталася помилка.")


     
      

@dp.message_handler(state=States.INPUT_TEXT)
async def process_encrypt(message: types.Message, state: FSMContext):
    plaintext = message.text
    if len(plaintext) > 200:
        await message.answer("Текст занадто довгий. Будь ласка, введіть текст довжиною не більше 200 символів.")
    else:
     ciphertext = box.encrypt(plaintext.encode('utf-8')).hex()
    await message.reply( f"Ваш зашифрованний текст: {ciphertext}")
    await state.finish()
    
@dp.message_handler(state=States.DECRYPT_TEXT)
async def process_decrypt(message: types.Message, state: FSMContext):
    encrypted_message = message.text
    try:
        decrypted_message = box.decrypt(bytes.fromhex(encrypted_message)).decode('utf-8')
        await message.reply(f"Ваш розшифрований текст: {decrypted_message}")
    except nacl.exceptions.CryptoError:
        await message.reply("Дешифрація не вдалася. Неправильний текст або ключі.")
    finally:
        await state.finish()



    
async def main():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main()) 
