import requests
from bs4 import BeautifulSoup as b
from url import URL, dict_
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time
import json

url = "https://taobao-tmall-product-detail.p.rapidapi.com/detail-product"

querystring = {"id":"678066325318"}

headers = {
	"X-RapidAPI-Key": "accdf5df4amsh89751d3c1d0c0f7p14d045jsnf78ca0e25d22",
	"X-RapidAPI-Host": "taobao-tmall-product-detail.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

obj = response.text
print(obj)

def find_prop(prop):
    start = obj.find(prop)
    print('start', start)
    print(obj[start:start + len(prop)])



find_prop('name')