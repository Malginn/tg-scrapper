import os
import shutil

from main import get_data_with_selenium

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hlink, link

from googletrans import Translator


API_TOKEN = '5692130473:AAFYtJiFHRfw2Rh1lLeDb1e7fxdywH3575U'

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# URL для тестов сделал
URL = 'https://m.tb.cn/h.UgFnSN4?tk=t6Cbd1rMSun'


def prepare_item(dict_value):
    string = f'''
Название: {dict_value['name']}\n
Продавец: {dict_value['seller']}\n
Цена: {split_(dict_value['price'], ' ')}\n
Размер: {split_(dict_value['size'], ' ')}\n
Доставка: {dict_value['delivery']}\n    
Цвет: {split_(dict_value['color'])}\n
Характеристика: {split_(dict_value['characteristic'])}\n
             '''    
#.split('¥')[1]+' ¥'

    return string

def split_(key, separator='\n'):
    string = separator.join(key)
    return string

def translate_text(data):
    translator = Translator()
    for k, v in data.items():
        if type(v) == list:
            for count, i in enumerate(data[k]):
                data[k][count] = translator.translate(i, src='zh-tw', dest='ru').text
        else:
            data[k] = translator.translate(v, src='zh-tw', dest='ru').text
    return data


# сделал обновленный перевод, твою функцию не трогал
# если ловил googletrans AttributeError: 'NoneType' object has no attribute 'group':
# pip install googletrans==4.0.0-rc1
# должно пофиксить
def translator_update(data):
    translator = Translator()
    if len(data['name']) > 0:
        data['name'] = translator.translate('Table', src='zh-tw', dest='ru').text
    else:
        data['name'] = 'Не найдено имя'

    if len(data['seller']) > 0:
        data['seller'] = translator.translate(data['seller'], src='zh-tw', dest='ru').text
    else:
        data['seller'] = 'Не найден продавец'

    new_characteristic = list()
    if len(data['characteristic']) > 0:
        for value in data['characteristic']:
            new_characteristic.append(translator.translate(value, src='zh-tw', dest='ru').text)
    else:
        data['characteristic'] = 'Не найдены характеристики'
    data['characteristic'] = new_characteristic

    new_color = list()
    if len(data['color']) > 0:
        for value in data['color']:
            new_color.append(translator.translate(value, src='zh-tw', dest='ru').text)
    else:
        new_color = 'Не найден цвет'
    data['color'] = new_color

    if len(data['delivery']) > 0:
        data['delivery'] = translator.translate(data['delivery'], src='zh-tw', dest='ru').text
    else:
        data['delivery'] = 'Не найдена доставка'

    new_size = list()
    if len(data['size']) > 0:
        for value in data['size']:
            new_size.append(translator.translate(value, src='zh-tw', dest='ru').text)
    else:
        new_size = 'Не найден размер'
    data['size'] = new_size

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
    # await message.answer(data['color'])
    hyper_link = f'<a href="{url}">Ссылка на товар</a>'
    # перевод и подготовка текста
    data = translator_update(data)
    prepare_data = prepare_item(data)

    # упаковка сообщения
    media = types.MediaGroup()
    if len(data['image']) > 0:
        for image in data['image']:
            if data['image'].index(image) == len(data['image'])-1:
                media.attach_photo(types.InputFile(f'./images/{image}'), f'{prepare_data}\n{hyper_link}', parse_mode="HTML")
            else:
                media.attach_photo(types.InputFile(f'./images/{image}'))
        await message.answer('фото есть')
    else:
        await message.answer('фото нет')

    # отправка результата
    
    await message.answer_media_group(media=media)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
