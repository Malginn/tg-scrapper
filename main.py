import urllib.request
import os
import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as condition
from selenium.common import NoSuchElementException, TimeoutException, JavascriptException

from colorama import Fore


def get_data_with_selenium(link):
    os.chdir('./')
    os.system('start browser.bat')
    time.sleep(3)

    dict_xpath = {'name': '//*[@class="tb-main-title"]',
                  'seller': '//*[contains(@class,"shop-name")]',
                  'price': '//*[@class="tb-rmb-num"]',
                  'size': '//*[@class="J_TSaleProp tb-clearfix"]/li/a/span',
                  'delivery': '//*[@id="J_WlServiceInfo"]',
                  'color': '//*[contains(@data-property,"颜色")]/li/a/span',
                  'characteristic': '//*[@class="attributes-list"]/li',
                  'image': '//*[@id="J_UlThumb"]/li/div/a/img'}

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_driver = "./chrome/chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)

    dict_value = {'name': '',
                  'seller': '',
                  'price': list(),
                  'size': list(),
                  'delivery': '',
                  'color': list(),
                  'characteristic': list(),
                  'image': list()
                  }

    try:
        driver.get(link)
        timeout = 40
        WebDriverWait(driver, timeout).until(condition.presence_of_element_located((By.XPATH, dict_xpath['name'])))

    except TimeoutException:
        print(Fore.RED + 'TimeoutException')

    except Exception as ex:
        print(ex)

    else:
        try:
            dict_value['name'] = driver.find_element(By.XPATH, dict_xpath['name']).text
        except NoSuchElementException:
            print(Fore.RED + 'Name not found')

        try:
            dict_value['seller'] = driver.find_element(By.XPATH, dict_xpath['seller']).text
        except NoSuchElementException:
            print(Fore.RED + 'Seller not found')

        try:
            prices = driver.find_elements(By.XPATH, dict_xpath['price'])
            for price in prices:
                dict_value['price'].append(price.text)
        except NoSuchElementException:
            print(Fore.RED + 'Price not found')

        try:
            sizes = driver.find_elements(By.XPATH, dict_xpath['size'])
            for size in sizes:
                dict_value['size'].append(size.text)
        except NoSuchElementException:
            print(Fore.RED + 'Size not found')

        try:
            dict_value['delivery'] = driver.find_element(By.XPATH, dict_xpath['delivery']).text
        except NoSuchElementException:
            print(Fore.RED + 'Delivery not found')

        try:
            colors = driver.execute_script("return Hub.config.get('sku').valItemInfo.propertyMemoMap")
            for color in colors.values():
                dict_value['color'].append(color)
        except JavascriptException:
            print(Fore.RED + 'Color not found')

        try:
            for characteristic in driver.find_elements(By.XPATH, dict_xpath['characteristic']):
                dict_value['characteristic'].append(characteristic.text)
        except NoSuchElementException:
            print(Fore.RED + 'Characteristics not found')

        try:
            images = driver.find_elements(By.XPATH, dict_xpath['image'])
            for image in images:
                img_50 = image.get_attribute('src')
                img_400 = img_50.replace('50x50.jpg_.webp', '400x400.jpg')
                dict_value['image'].append(download(img_400, images.index(image)))
        except NoSuchElementException:
            print(Fore.RED + 'Images not found')

    finally:

        driver.close()
        driver.quit()
        return dict_value


def download(url, num):
    resource = urllib.request.urlopen(url)
    with open(f"./images/test{num}.jpg", 'wb') as out:
        out.write(resource.read())
    return f'test{num}.jpg'
