import re
from os import environ
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

CAPABILITIES = {
            'browserName': 'chrome',
            'enableVNC': True,
            'enableVideo': False,
        }


def get_creative_ballance(username: str, password: str) -> int:
    driver = webdriver.Remote(
            command_executor=environ.get('DRIVER_URL'),
            desired_capabilities=CAPABILITIES,
        )
    driver.get('https://creativemarket.com/sign-in')
    input_username = driver.find_element_by_xpath("//input[@name='username']")
    input_username.send_keys(username)
    input_pass = driver.find_element_by_xpath("//input[@name='password']")
    input_pass.send_keys(password)
    sleep(1)
    log_button = driver.find_element_by_xpath("//form/button")
    log_button.click()
    sleep(3)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    driver.close()
    ballance = soup.find(
        'div', attrs={"class": "header__user-credits-wrapper"}
    ).find(
        'span', attrs={'class': 'sp-body'}
    ).text.strip()
    ballance_nums = re.findall(r'\d', ballance)[:-2]
    return int(''.join(ballance_nums))


def get_elements_ballance(username: str, password: str) -> int:
    driver = webdriver.Remote(
            command_executor=environ.get('DRIVER_URL'),
            desired_capabilities=CAPABILITIES,
        )
    driver.get('https://elements-contributors.envato.com/sign-in')
    input_username = WebDriverWait(driver, timeout=20).until(
        lambda d: d.find_element_by_xpath("//input[@name='username']")
    )
    input_username.send_keys(username)
    input_pass = driver.find_element_by_xpath("//input[@name='password']")
    input_pass.send_keys(password)
    sleep(2)
    log_button = driver.find_element_by_xpath("//form/button")
    log_button.click()
    WebDriverWait(driver, timeout=20).until(
        lambda d: d.find_element_by_xpath("//a[@href='/sign-out']")
    )
    driver.get('https://elements-contributors.envato.com/account/earnings')
    WebDriverWait(driver, timeout=20).until(
        lambda d: d.find_element_by_xpath("//p[contains(text(), 'Total Payout')]")
    )
    soup = BeautifulSoup(driver.page_source, 'lxml')
    driver.close()
    ballance = soup.find(
        'div', attrs={'class': re.compile(r"^TotalEarnings__heading.*")}
    ).text.strip()
    ballance_nums = re.findall(r'\d', ballance)[:-2]
    return int(''.join(ballance_nums))
