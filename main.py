import urllib.request
import base64

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException

from colorama import Fore

# import time


def get_data_with_selenium(link):
    dict_xpath = {'name': '//*[@class="tb-main-title"]',
                  'seller': '//*[@class="tb-shop-name"]',
                  'price': '//*[@class="tb-rmb-num"]',
                  'size': '//*[@data-property="尺码"]/li/a/span',
                  'delivery': '//*[@id="J_WlServiceInfo"]',
                  'color': '//*[@data-property="颜色分类"]/li/a/span',
                  'characteristic': '//*[@class="attributes-list"]/li',
                  'image': '//*[@id="description"]/div/table/tbody/tr/td/img'}
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_driver = "./chrome/chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
    dict_value = {'name': '',
                  'seller': '',
                  'price': list(),
                  'size': list(),
                  'delivery': '',
                  'color': '',
                  'characteristic': list(),
                  'image': list()
                  }
    try:
        # driver.get(link)
        # time.sleep(10)
        pass

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
            dict_value['color'] = driver.find_element(By.XPATH, dict_xpath['color']).text
        except NoSuchElementException:
            print(Fore.RED + 'Color not found')

        try:
            for characteristic in driver.find_elements(By.XPATH, dict_xpath['characteristic']):
                dict_value['characteristic'].append(characteristic.text)
        except NoSuchElementException:
            print(Fore.RED + 'Characteristics not found')

        try:
            images = driver.find_elements(By.XPATH, dict_xpath['image'])
            for image in images:
                dict_value['image'].append(download(image.get_attribute('src')))
        except NoSuchElementException:
            print(Fore.RED + 'Images not found')

    finally:
        # driver.close()
        # driver.quit()
        return dict_value


def download(url):
    resource = urllib.request.urlopen(url)
    image = base64.b64encode(resource.read())
    # for decode use:
    # base64.b64decode(image)
    return image


def main():
    link = ''
    data = get_data_with_selenium(link)
    print(Fore.GREEN + 'dump finally ready')


if __name__ == '__main__':
    main()
