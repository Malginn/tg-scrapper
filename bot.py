from aiogram import Bot, Dispatcher, executor, types
# from url import dict_
from main import get_data_with_selenium
import os
import shutil

from googletrans import Translator
translator = Translator()

API_TOKEN = '5692130473:AAFYtJiFHRfw2Rh1lLeDb1e7fxdywH3575U'

# URL для тестов сделал
URL = 'https://m.tb.cn/h.UgFnSN4?tk=t6Cbd1rMSun'


def prepare_item(dict_value):
    string = f'''
Название: {dict_value['name']}\n
Продавец: {dict_value['seller']}\n
Цена: {price_split(dict_value)}\n
Размер: {dict_value['size']}\n
Доставка: {dict_value['delivery']}\n
Цвет: {dict_value['color']}\n
Характеристика: {charac(dict_value)}\n
             '''    # 'Картинка': {dict_value['image']

    return string


def charac(data):
    str_ch = '\n'.join(data['characteristic']) 
    return str_ch


def price_split(data):
    str_pr = ' '.join(data['price'])
    return str_pr


def translate_text(data):
    for k, v in data.items():
        if type(v) == list:
            for count, i in enumerate(data[k]):
                data[k][count] = translator.translate(i, src='zh-tw', dest='ru').text
        else:
            data[k] = translator.translate(v, src='zh-tw', dest='ru').text
    return data


def clear_img():
    shutil.rmtree('./images/')
    os.makedirs('./images/')
    # os.remove(file)


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message):
    await message.answer("Hi!")


@dp.message_handler()
async def all_msg_handler(message: types.Message):
    text = message.text
    data = get_data_with_selenium(text)  # URL заменить на message.text
    media = types.MediaGroup()
    for image in data['image']:
        if data['image'].index(image) == len(data['image'])-1:
            media.attach_photo(types.InputFile(f'./images/{image}'), )  # text заменить на результат обработки data   , prepare_item(data)
        else:
            media.attach_photo(types.InputFile(f'./images/{image}'))
    await message.answer_media_group(media=media)
    print('sent photo')
    data = translate_text(data)
    print('text translated')
    await message.answer(f'{prepare_item(data)}\n{text}')
    print('text sent')
    clear_img()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
