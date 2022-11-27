import urllib.request
import os
import time
import logging

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as condition
from selenium.common import NoSuchElementException, TimeoutException, JavascriptException

from colorama import Fore
import requests
from requests import HTTPError
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_data_with_selenium(link):
    os.chdir('./')
    os.system('start browser.bat')
    time.sleep(3)

    dict_xpath = {'name': '//*[@class="tb-main-title"]',
                  # 'seller': '//*[contains(@class,"shop-name")]',
                  'price': '//*[@class="tb-rmb-num"]',
                  'size': '//*[@class="J_TSaleProp tb-clearfix"]/li/a/span',
                  'delivery': '//*[@id="J_WlServiceInfo"]',
                  'color': '//*[contains(@data-property,"颜色")]/li/a/span',
                  'characteristic': '//*[@class="attributes-list"]/li',
                  'image': '//*[@id="J_UlThumb"]/li/div/a/img',
                  'video': '//*[@class="lib-video"]/video/source'}

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_driver = "./chrome/chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)

    dict_value = {'name': '',
                  # 'seller': '',
                  'price': list(),
                  'size': list(),
                  'delivery': '',
                  'color': list(),
                  'characteristic': list(),
                  'image': list(),
                  'video': ''
                  }

    try:
        driver.get(link)
        timeout = 40
        WebDriverWait(driver, timeout).until(condition.presence_of_element_located((By.XPATH, dict_xpath['name'])))

    except TimeoutException:
        logger.debug('TimeoutException')
        print(Fore.RED + 'TimeoutException')

    except Exception as ex:
        print(ex)

    else:
        try:
            dict_value['name'] = driver.find_element(By.XPATH, dict_xpath['name']).text
        except NoSuchElementException:
            logger.debug('Name not found')

        # try:
        #     dict_value['seller'] = driver.find_element(By.XPATH, dict_xpath['seller']).text
        # except NoSuchElementException:
        #     print(Fore.RED + 'Seller not found')

        try:
            prices = driver.find_elements(By.XPATH, dict_xpath['price'])
            for price in prices:
                dict_value['price'].append(price.text)
        except NoSuchElementException:
            logger.debug('Price not found')

        try:
            sizes = driver.find_elements(By.XPATH, dict_xpath['size'])
            for size in sizes:
                dict_value['size'].append(size.text)
        except NoSuchElementException:
            logger.debug('Size not found')

        try:
            dict_value['delivery'] = driver.find_element(By.XPATH, dict_xpath['delivery']).text
        except NoSuchElementException:
            logger.debug('Delivery not found')

        try:
            colors = driver.execute_script("return Hub.config.get('sku').valItemInfo.propertyMemoMap")
            for color in colors.values():
                dict_value['color'].append(color)
        except JavascriptException:
            logger.debug('Color not found')

        try:
            for characteristic in driver.find_elements(By.XPATH, dict_xpath['characteristic']):
                dict_value['characteristic'].append(characteristic.text)
        except NoSuchElementException:
            logger.debug('Characteristics not found')

        try:
            logger.debug('Try to found images')
            images = driver.find_elements(By.XPATH, dict_xpath['image'])
            for image in images:
                img_50 = image.get_attribute('src')
                img_400 = img_50.replace('50x50.jpg_.webp', '400x400.jpg')
                value = download_img(img_400, images.index(image), prefix='first')
                dict_value['image'].append(value)
        except NoSuchElementException:
            logger.debug('Images not found')

        try:
            logger.debug('Try to found images 2')
            image_json_link = driver.execute_script("return Hub.config.get('desc').apiImgInfo")
            img_names = download_img_name(image_json_link.replace('//', 'http://'))
            for name in img_names:
                while True:
                    try:
                        value = download_img(prepare_link(name), img_names.index(name), prefix='second')
                        dict_value['image'].append(value)
                    except HTTPError:
                        pass
                    else:
                        break
        except JavascriptException:
            logger.debug('Images 2 not found')

        try:
            logger.debug('Try to found videos')
            video_id = driver.execute_script("return Hub.config.get('video').videoId")
            video_url = f"http://cloud.video.taobao.com/play/u/2620439306/p/1/e/6/t/1/{video_id}.mp4'"
            dict_value['video'] = download_video(video_url)
        except JavascriptException:
            logger.debug('Video not found')

    finally:

        driver.close()
        driver.quit()
        return dict_value


def download_img(url, num, prefix='test'):
    resource = urllib.request.urlopen(url)
    with open(f"./images/{prefix}{num}.jpg", 'wb') as out:
        out.write(resource.read())
    return f'{prefix}{num}.jpg'


def download_video(url):
    resource = urllib.request.urlopen(url)
    with open("./videos/video.mp4", 'wb') as out:
        out.write(resource.read())
    return f'video.mp4'


def download_img_name(image_json_link):
    r = requests.get(image_json_link)
    image_fucking_dict = json.loads(r.text[14:-1])
    image_name_list = []
    for k in image_fucking_dict.keys():
        image_name_list.append(k)
    image_name_list = image_name_list[4:]
    return image_name_list


def prepare_link(json_name):
    prefix = json_name.split('!!')[1]
    prefix = prefix[:-4]
    link = f'https://img.alicdn.com/imgextra/i1/{prefix}/{json_name}'
    return link
