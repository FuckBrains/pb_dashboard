from selenium import webdriver
from time import sleep
import json
from os import environ


def get() -> webdriver.Remote:
    capabilities = {
            'browserName': 'chrome',
            'enableVNC': True,
            'enableVideo': False,
        }
    browser_options = webdriver.chrome.options.Options()
    browser_options.add_extension('anticaptcha.crx')
    driver = webdriver.Remote(
            command_executor=environ.get('DRIVER_URL'),
            desired_capabilities=capabilities,
            options=browser_options,
        )
    driver.get('https://antcpt.com/blank.html')
    message = {
            'receiver': 'antiCaptchaPlugin',
            'type': 'setOptions',
            'options': {'antiCaptchaApiKey': environ.get('AC_KEY')},
        }
    sleep(10)
    driver.execute_script(
        'return window.postMessage({});'.format(json.dumps(message)),
    )
    sleep(5)
    return driver
