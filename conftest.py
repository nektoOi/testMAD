import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import sys
import allure
import configparser
import os
from selenium.webdriver.common.by import By
import configparser
import os
import allure
import requests



@pytest.fixture(scope="class", autouse=True)
def initWebDriver():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=2000,1200")
    ser = Service("G:\\chromedriver.exe")
    driver = webdriver.Chrome(service=ser, options=chrome_options)
    driver.implicitly_wait(5)
    #driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture(scope="class", autouse=False)
def auth_unik_convertation(initWebDriver):
    driver = initWebDriver
    initWebDriver.get('https://test.test.ru/sign-in')
    time.sleep(1)
    initWebDriver.find_element_by_xpath('//input[@name= "email"]').send_keys('test')
    initWebDriver.find_element_by_xpath('//input[@name= "password"]').send_keys('test')
    initWebDriver.find_element_by_xpath('//button[@type= "submit"]').click()
    time.sleep(1)
    config = configparser.ConfigParser()
    try:

        config.read("settings.ini", "utf8")
        external_id = config['unicredit'].get('external_client_for_convertation')
        domen_lk = config['unicredit'].get('domen_lk')
    except:
        config.read("../settings.ini", "utf8")
        external_id = config['unicredit'].get('external_client_for_convertation')
        domen_lk = config['unicredit'].get('domen_lk')
    initWebDriver.get('https://admin.gopoints.ru/supervisor')
    initWebDriver.find_element_by_xpath('//input[@placeholder= "domain"]').send_keys(domen_lk)
    initWebDriver.find_element_by_xpath('//input[@placeholder= "external ID"]').send_keys(external_id)

    initWebDriver.find_element_by_xpath('//button[@class= "bp3-button bp3-intent-primary"]').click()
    time.sleep(1)

    initWebDriver.switch_to.window(initWebDriver.window_handles[0])
    url = initWebDriver.find_element_by_xpath('//b').text
    print(url)

    yield url
