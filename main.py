import requests
from bs4 import BeautifulSoup as b
from url import URL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time

# def get_data(url):
#     headers = {
#         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#         'accept-encoding' : 'gzip, deflate, br',
#         'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,cs;q=0.6',
#         'cache-control': 'max-age=0',
#         'cookie': 'cna=wa73Gy1qi20CASWTezySQUFm; xlly_s=1; _samesite_flag_=true; cookie2=1f99c936921103dc9da622396e9157b6; t=9e5fa9b2c5c3f7723b4392c01a76c85b; _tb_token_=7746b3b6130e7; mt=ci%3D-1_1; thw=xx; hng=GLOBAL%7Czh-CN%7CUSD%7C999; _gcl_au=1.1.1884281658.1668335125; _uetsid=79b7eb10633d11edaf93e7f86d5722cd; _uetvid=79b82480633d11edab0105892dccd22e; _m_h5_tk=4b2225f39ab286ee1dd5e660e059b079_1668342435110; _m_h5_tk_enc=4032505da6c6f171cbcd5521ce59a278; v=0; sgcookie=E10031wHbq%2BVwem9ROoSpcUoxROeK%2FII%2FUXh93NkbFiPctIzGh3rFWebz%2B7DLF6TTo1zmdCougFPW%2BYgg%2BVzaYp0NFYesYTMipMnr9xCI5p%2Btqw%3D; uc3=vt3=F8dCvjXuiRbytUG4qLs%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D&id2=UUpgQymtGJ2Zcj1Ghg%3D%3D&nk2=F5RCZsMuJlX8S8ISJTI%3D; csg=ddb9cbd9; lgc=tb738241964524; cancelledSubSites=empty; dnk=tb738241964524; skt=1b179cfca7b125cb; existShop=MTY2ODMzNTM3NQ%3D%3D; uc4=id4=0%40U2gqzJ90TuA7pv8TyVY%2BG7B9FQcM7mWt&nk4=0%40FY4JiMy53AS88ctv22XS6ZLldCeGQAo9OA%3D%3D; tracknick=tb738241964524; _cc_=UtASsssmfA%3D%3D; uc1=cookie21=U%2BGCWk%2F7oPIg&pas=0&existShop=false&cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D&cookie14=UoeyBrggvJaK6Q%3D%3D; tfstk=cD_5BeTmdYD5C-4nrLN4LezH1gTGZFyXiu9RN8NpNY6nad15itgwCiShxxYe9I1..; l=eBL3WX9qTyL-4DOzoOfahurza77OSIRvDuPzaNbMiOCP_cCe5OHdW6zAr98wC3MNh67JR3r0glSeBeYBqI2wsWRKe5DDwQHmn; isg=BICAePpk9zNxzos3asQ2sp2PUQ5SCWTTGMzxWvoRTBsudSCfohk0Y1ZHicW1ERyr',

#         'connection': 'keep-alive',
#         'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36'
#     }

    # r = requests.get(url=URL, headers=headers)

    # with open('index.html', 'w', encoding='utf-8') as file:
    #     file.write(r.text)


def get_data_with_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-software-rasterizer')
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # options.add_argument('general.useragent.override', 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36')

    try:
        driver = webdriver.Chrome(
            executable_path='../ozon/chrome/chromedriver.exe',
            options=options
        )
        driver.get(url)
        time.sleep(120)
        delay = 0.05 # seconds
        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")

        try:
            time.sleep(30)

            element = driver.find_element(By.XPATH, '/html/body/div[9]/div[2]/div')
            print('click')
            driver.execute_script("arguments[0].click();", element)
                #tab-active-index-0 tb-detail w990
            name = driver.find_element(By.XPATH, '//*[@id="J_Title"]/h3')
            print(name.text)

            time.sleep(10)
        except Exception as ex:
            print(ex)

        with open('index_selenium.html', 'w', encoding='utf-8') as file:
            file.write(driver.page_source)
        
        

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()




def main():
    # get_data(URL)
    get_data_with_selenium(URL)



if __name__ == '__main__':
    main()