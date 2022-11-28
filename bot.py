from main import get_data_with_selenium

from aiogram import Bot, Dispatcher, executor, types
from auth_data import TOKEN

from googletrans import Translator

translator = Translator()

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def prepare_item(dict_value):
    string = (f"Название: {dict_value['name']}\n",
              f"Цена: {is_exist_fun(dict_value['price'], ' ')}\n",
              f"Размер: {is_exist_fun(dict_value['size'], ' ')}\n",
              f"Доставка: {dict_value['delivery']}\n",
              f"Цвет: {is_exist_fun(dict_value['color'], ' ')}\n",
              f"Характеристика: {is_exist_fun(dict_value['characteristic'])}\n")
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


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message):
    await message.answer("Hi!")


@dp.message_handler()
async def all_msg_handler(message: types.Message):
    # берем url с сообщения
    url = message.text
    data = get_data_with_selenium(url)

    # перевод и подготовка текста
    print('translation')
    data = translator_update(data)
    prepare_data = prepare_item(data)
    hyper_link = f'<a href="{url}">Ссылка на товар</a>'
    print('send photo')
    await send_photo(data['image'], message)
    print('send video')
    await send_video(data['video'], message)
    print('send text')
    await send_text(prepare_data, hyper_link, message)


async def send_photo(images, message):
    media = types.MediaGroup()
    for image in images:
        media.attach_photo(types.InputFile(f'./images/{image}'))
        if images.index(image) % 10 == 9 or images.index(image) == len(images)-1:
            await message.answer_media_group(media=media)
            media = types.MediaGroup()


async def send_video(video, message):
    if video != '':
        media = types.MediaGroup()
        media.attach_video(types.InputFile(f'./videos/{video}'))
        await message.answer_media_group(media=media)


async def send_text(data, hlink, message):
    index = 5
    while len(data[:index]) > 1024:
        index -= 1
    if index < 5:
        msg = ''
        for i in range(index):
            msg += data[i]
        await message.answer(msg)
        msg = ''
        for i in range(index, 6):
            msg += data[i]
        msg += hlink
        await message.answer(msg, parse_mode='HTML')
    else:
        msg = ''
        for i in range(6):
            msg += data[i]
        msg += hlink
        await message.answer(msg, parse_mode='HTML')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
