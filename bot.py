import os
import shutil

from main import get_data_with_selenium

from aiogram import Bot, Dispatcher, executor, types

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
Цена: {price_split(dict_value)}\n
Размер: {dict_value['size']}\n
Доставка: {dict_value['delivery'].split('¥')[1]+' ¥'}\n
Цвет: {dict_value['color']}\n
Характеристика: {charac(dict_value)}\n
             '''

    return string


def charac(data):
    str_ch = '\n'.join(data['characteristic']) 
    return str_ch


def price_split(data):
    str_pr = ' '.join(data['price'])
    return str_pr


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
        data['characteristic'] = 'Не найдены харакетиристики'
    data['characteristic'] = new_characteristic

    if len(data['color']) > 0:
        data['color'] = translator.translate(data['color'], src='zh-tw', dest='ru').text
    else:
        data['color'] = 'Не найден цвет'
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
    data = get_data_with_selenium('https://item.taobao.com/item.htm?spm=a1z10.5-c-s.w4002-22637139779.40.3834709dUCU5ow&id=692133878189')

    # перевод и подготовка текста
    data = translator_update(data)
    prepare_data = prepare_item(data)

    # упаковка сообщения
    media = types.MediaGroup()
    if len(data['image']) > 0:
        for image in data['image']:
            if data['image'].index(image) == len(data['image'])-1:
                media.attach_photo(types.InputFile(f'./images/{image}'), prepare_data)
            else:
                media.attach_photo(types.InputFile(f'./images/{image}'))
        await message.answer('фото есть')
    else:
        await message.answer('фото нет')

    # отправка результата
    
    # await message.answer_media_group(media=media)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
