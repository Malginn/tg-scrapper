import os
import shutil

from main import get_data_with_selenium

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hlink, link

from googletrans import Translator
translator = Translator()


API_TOKEN = '5692130473:AAFYtJiFHRfw2Rh1lLeDb1e7fxdywH3575U'

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# URL для тестов сделал
URL = 'https://m.tb.cn/h.UgFnSN4?tk=t6Cbd1rMSun'


def prepare_item(dict_value):
    string = f'''
Название: {dict_value['name']}\n

Цена: {is_exist_fun(dict_value['price'], ' ')}\n
Размер: {is_exist_fun(dict_value['size'], ' ')}\n
Доставка: {dict_value['delivery']}\n    
Цвет: {is_exist_fun(dict_value['color'], ' ')}\n
Характеристика: {is_exist_fun(dict_value['characteristic'])}\n
             '''    
#.split('¥')[1]+' ¥'
#Продавец: {dict_value['seller']}\n
    return string

def split_(key, separator='\n'):
    string = separator.join(key)
    return string


def is_exist_fun(key, separator='\n'):
    if 'Not' in key:
        return key
    elif type(key) != list:
        return key
    return split_(key, separator)


# def translate_text(data):
#     translator = Translator()
#     for k, v in data.items():
#         if type(v) == list:
#             for count, i in enumerate(data[k]):
#                 data[k][count] = translator.translate(i, src='zh-tw', dest='ru').text
#         else:
#             data[k] = translator.translate(v, src='zh-tw', dest='ru').text
#     return data


# сделал обновленный перевод, твою функцию не трогал
# если ловил googletrans AttributeError: 'NoneType' object has no attribute 'group':
# pip install googletrans==4.0.0-rc1
# должно пофиксить

def validation_for_translate(data: dict, key: str):
    if key in ['name', 'delivery', 'seller']:
        if data[key]:
            data[key] = translator.translate(data[key], src='zh-tw', dest='ru').text
        else:
            data[key] = f'Not found {key}'
            
    else:
        new_item = list()
        if data[key]:
            for value in data[key]:
                new_item.append(translator.translate(value, src='zh-tw', dest='ru').text)
        else:
            data[key] = f'Not found {key}'
        data[key] = new_item

    return data

def translator_update(data):

    for i in ['name', 'delivery', 'size', 'characteristic', 'color', 'price']:
        if i in data.keys():
            data = validation_for_translate(data, i)

    return data


# удалять не стал, но функция юзлес, ибо мы передаем список имен фото
# старые фотки перезаписываются на новые и память соответственно не засоряется
def clear_img():
    shutil.rmtree('./images/')
    os.makedirs('./images/')
    # os.remove(file)


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message):
    await message.answer("Hi!")


@dp.message_handler()
async def all_msg_handler(message: types.Message):
    # берем url с сообщения и парсим сайт
    url = message.text
    data = get_data_with_selenium(url)

    # перевод и подготовка текста
    data = translator_update(data)
    prepare_data = prepare_item(data)
    hyper_link = f'<a href="{url}">Ссылка на товар</a>'

    # #сокращаем текст для отправки сообщения
    while len(prepare_data) > 1024:
        data['characteristic'] = data['characteristic'].pop()
        prepare_data = prepare_item(data)

    # упаковка сообщения
    media = types.MediaGroup()
    if len(data['image']) > 0:
        for image in data['image']:
            if data['image'].index(image) == len(data['image'])-1:
                media.attach_photo(types.InputFile(f'./images/{image}'), f'{prepare_data}\n{hyper_link}', parse_mode="HTML")
            else:
                media.attach_photo(types.InputFile(f'./images/{image}'))
    else:
        await message.answer('Фото нет, товара не будет')

    # отправка результата
    
    await message.answer_media_group(media=media)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
