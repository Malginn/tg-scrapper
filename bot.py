from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = '5692130473:AAFYtJiFHRfw2Rh1lLeDb1e7fxdywH3575U'

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message):
    await message.answer("Hi!")


@dp.message_handler()
async def all_msg_handler(message: types.Message):
    text = message.text


def parser(link):
    pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
