import os
import shutil

from main import get_data_with_selenium

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hlink, link
from auth_data import TOKEN

from googletrans import Translator
translator = Translator()


# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# URL для тестов сделал
# URL = 'https://m.tb.cn/h.UgFnSN4?tk=t6Cbd1rMSun'


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


def add_img(key, media, prepare_data, hyper_link, is_first):
    if is_first:
        for image in key:
            if key.index(image) == len(key)-1:
                media.attach_photo(types.InputFile(f'./images/{image}'), f'{prepare_data}\n{hyper_link}', parse_mode="HTML")
            else:
                media.attach_photo(types.InputFile(f'./images/{image}'))

    else:
        media = types.MediaGroup()
        for image in key:
            media.attach_photo(types.InputFile(f'./images/{image}'))

def add_video(media, key):
    for video in key:
        media.attach_video(types.InputFile(f'./video/{video}'))
    
# удалять не стал, но функция юзлес, ибо мы передаем список имен фото
# старые фотки перезаписываются на новые и память соответственно не засоряется
def clear_img():
    shutil.rmtree('./images/')
    os.makedirs('./images/')

def clear_video():
    shutil.rmtree('./video/')
    os.makedirs('./video/')



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

    # сокращаем текст для отправки сообщения
    while len(prepare_data) > 1024:
        data['characteristic'] = data['characteristic'].pop()
        prepare_data = prepare_item(data)

    # упаковка сообщения
    media = types.MediaGroup()
    if len(data['image']) > 0:
        if len(data['image']) + len(data['video']) < 11:
            # for image in data['image']:
            #     if data['image'].index(image) == len(data['image'])-1:
            #         media.attach_photo(types.InputFile(f'./images/{image}'), f'{prepare_data}\n{hyper_link}', parse_mode="HTML")
            #     else:
            #         media.attach_photo(types.InputFile(f'./images/{image}'))
            add_img(data['image'], media, prepare_data, hyper_link, is_first=True)
            if data['video'] > 0: 
                add_video(media, data['video']) 
            else: 
                pass

            await message.answer_media_group(media=media)
        

        elif len(data['image']) + len(data['video']) <21:
            #дробим картинки на два массива и отправляем по отдельности
            first_img = data['image'][ : len(data['image'])/2]
            second_img = data['image'][len(data['image'])/2 : ]

            first_media = add_img(first_img, media, prepare_data, hyper_link, is_first=True)
            second_media = add_img(second_img, media, prepare_data, hyper_link, is_first=False)
            if data['video'] > 0: 
                add_video(first_media, data['video']) 
            else: 
                pass

            await message.answer_media_group(media=first_media)
            await message.answer_media_group(media=second_media)


        else:
            await message.answer('Картинок больше 20 ;(')

    else:
        await message.answer('Фото нет, товара не будет')

    clear_img()
    clear_video()



    # отправка результата
    
    


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
