from pb_parsers import renew, parsers, browser
from time import sleep
import requests
from os import environ
import traceback


def main():
    driver = browser.get()
    eurusd = parsers.get_eurusd_rate()
    renew.creative_balance(driver)
    renew.elements_balance(driver)
    renew.freepik_balance(driver, eurusd)


while True:
    try:
        main()
    except:
        err_msg = 'pb_dashboard:{}'.format(traceback.format_exc())
        requests.post(
            'https://api.telegram.org/bot{token}/sendMessage?chat_id={tui}&text={text}'.format(
                token=environ.get('ALLERT_BOT_TOKEN'),
                tui=environ.get('ADMIN_TUI'),
                text=err_msg,
            ))
    sleep(3600)
