from aiogram import Bot, Dispatcher, executor, types
from url import dict_
from main import get_data_with_selenium
import os
import shutil

from googletrans import Translator
translator = Translator()

API_TOKEN = '5692130473:AAFYtJiFHRfw2Rh1lLeDb1e7fxdywH3575U'

# URL для тестов сделал
URL = 'https://item.taobao.com/item.htm?id=687815414870&price=194.99&sourceType=item&sourceType=item&suid=f4ab6dfd-3c89-4606-81a7-b9b74ad5adb9&ut_sk=1.YgbGi%2FkQyU0DAD3WQG9i%2BcAZ_21646297_1668264784118.Copy.ShareGlobalNavigation_1&un=75b8c07d63d793d3b869032d15dddb3f&share_crt_v=1&un_site=0&spm=a2159r.13376460.0.0&sp_abtk=gray_ShareGlobalNavigation_1_code_simpleAndroid&tbSocialPopKey=shareItem&sp_tk=dDZDYmQxck1TdW4%3D&cpp=1&shareurl=true&short_name=h.UgFnSN4&bxsign=scd7fVjWiuAdaVF9IWPRnH-aVCofWKHVNbA9YOC3YWLrrDMwNZgLit2jZUBIBDj6aNhOlcPfcXr_odogmSCQeRh6J4dKjZVoBf6uA-NLYQRYgB-5yC2nYyX5N4fDyv9RViOgmgYDKfBaP4phh2IL6qczQ&tk=t6Cbd1rMSun&app=chrome&price=194.99&sourceType=item&sourceType=item&suid=f4ab6dfd-3c89-4606-81a7-b9b74ad5adb9&ut_sk=1.YgbGi%2FkQyU0DAD3WQG9i%2BcAZ_21646297_1668264784118.Copy.ShareGlobalNavigation_1&un=75b8c07d63d793d3b869032d15dddb3f&share_crt_v=1&un_site=0&spm=a2159r.13376460.0.0&sp_abtk=gray_ShareGlobalNavigation_1_code_simpleAndroid&tbSocialPopKey=shareItem&sp_tk=dDZDYmQxck1TdW4%3D&cpp=1&shareurl=true&short_name=h.UgFnSN4&bxsign=scd7fVjWiuAdaVF9IWPRnH-aVCofWKHVNbA9YOC3YWLrrDMwNZgLit2jZUBIBDj6aNhOlcPfcXr_odogmSCQeRh6J4dKjZVoBf6uA-NLYQRYgB-5yC2nYyX5N4fDyv9RViOgmgYDKfBaP4phh2IL6qczQ&tk=t6Cbd1rMSun&app=chrome'


def prepare_item(dict_value):
    string = f'''
Название: {dict_value['name']}\n
Продавец: {dict_value['seller']}\n
Цена: {price_split()}\n
Размер: {dict_value['size']}\n
Доставка: {dict_value['delivery']}\n
Цвет: {dict_value['color']}\n
Характеристика: {charac()}\n
             '''    # 'Картинка': {dict_value['image']

    return string


def charac():
    str_ch = '\n'.join(dict_['characteristic']) 
    return str_ch


def price_split():
    str_pr = ' '.join(dict_['price'])
    return str_pr


def translate_text():
    for k, v in dict_.items():
        if type(v) == list:
            for count, i in enumerate(dict_[k]):
                dict_[k][count] = translator.translate(i, src='zh-tw', dest='ru').text
        else:
            dict_[k] = translator.translate(v, src='zh-tw', dest='ru').text
        return dict_


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
    data = get_data_with_selenium(URL)  # URL заменить на message.text
    media = types.MediaGroup()
    for image in data['image']:
        if data['image'].index(image) == len(dict_['image'])-1:
            media.attach_photo(types.InputFile(f'./images/{image}'), text)  # text заменить на результат обработки data
        else:
            media.attach_photo(types.InputFile(f'./images/{image}'))
    await message.answer_media_group(media=media)
    clear_img()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
