import re
from time import sleep
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def get_eurusd_rate() -> float:
    soup = BeautifulSoup(requests.get('https://www.google.com/finance/quote/EUR-USD').content)
    eur_usd = soup.find('div', attrs={'class': 'YMlKec fxKbKc'}).text
    return float(''.join(eur_usd))


def get_creative_ballance(driver: webdriver.Remote, username: str, password: str) -> int:
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
    driver.delete_all_cookies()
    ballance = soup.find(
        'div', attrs={"class": "header__user-credits-wrapper"}
    ).find(
        'span', attrs={'class': 'sp-body'}
    ).text.strip()
    ballance_nums = re.findall(r'\d', ballance)[:-2]
    return int(''.join(ballance_nums))


def get_elements_ballance(driver: webdriver.Remote, username: str, password: str) -> int:
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
    driver.delete_all_cookies()
    ballance = soup.find(
        'div', attrs={'class': re.compile(r".*TotalEarnings__totalPayout.*")}
    ).find(
        'div', attrs={'class': re.compile(r"^TotalEarnings__heading.*")}
    ).text.strip()
    ballance_nums = re.findall(r'\d', ballance)[:-2]
    return int(''.join(ballance_nums))


def get_freepik_ballance(driver: webdriver.Remote, username: str, password: str) -> int:
    driver.get('https://id.freepikcompany.com/login?client_id=freepik_contributor&action=login')
    input_username = WebDriverWait(driver, timeout=20).until(
        lambda d: d.find_element_by_xpath("//input[@name='username']")
    )
    input_username.send_keys(username)
    input_pass = driver.find_element_by_xpath("//input[@name='password']")
    input_pass.send_keys(password)
    sleep(2)
    log_button = driver.find_element_by_xpath("//form/button")
    log_button.click()
    WebDriverWait(driver, timeout=120).until(
        lambda d: d.find_element_by_xpath("//a[@href='/oauth/logout']")
    )
    driver.get('https://contributor.freepik.com/dashboard')
    sleep(5)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    driver.delete_all_cookies()
    ballance = soup.find(
        'div', attrs={'class': 'current-month'}
    ).find(
        'h1', attrs={'class': 'text__state--green'}
    ).text
    ballance_nums = re.findall(r'\d', ballance)
    return int(''.join(ballance_nums))
