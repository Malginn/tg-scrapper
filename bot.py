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

def prepare_item(dict_value):
    string = f'''
                Название: {dict_value['name']}\n
                Продавец: {dict_value['seller']}\n
                Цена: {price_split(dict_value['price'])}\n
                Размер: {dict_value['size']}\n
                Доставка: \n{dict_value['delivery']}\n
                Цвет: {dict_value['color']}\n
                Характеристика: {charac()}\n
                

             '''    #'Картинка': {dict_value['image']

    return string

def charac():
    str_ch = '\n'.join(dict_['characteristic'])
    # for i in dict_['characteristic']:
    #     str_ch.join(i)
    
    return str_ch

def price_split(prices):
    pass

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
