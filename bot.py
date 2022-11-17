from aiogram import Bot, Dispatcher, executor, types
from url import dict_
from main import main
import base64

from googletrans import Translator
translator = Translator()

def prepare_item(dict_value):
    string = f'''
Название: {dict_value['name']}\n
Продавец: {dict_value['seller']}\n
Цена: {price_split()}\n
Размер: {dict_value['size']}\n
Доставка: {dict_value['delivery']}\n
Цвет: {dict_value['color']}\n
Характеристика: {charac()}\n
             '''    #'Картинка': {dict_value['image']

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
    dict_ = main()  #text

    # await message.answer_photo(message.chat.id, photo=photo, caption="text")
    media = types.MediaGroup()
    images = [base64.b64decode(i) for i in dict_['image']]
    
    for num, img in enumerate(images):
        media.attach_photo(types.InputMediaPhoto(img, caption = prepare_item(dict_) if num == 0 else ''))
        await message.answer_media_group(media=media)






if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

