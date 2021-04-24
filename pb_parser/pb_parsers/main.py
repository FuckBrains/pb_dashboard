from pb_parsers import renew
from time import sleep

while True:
    renew.creative_balance()
    sleep(30)
    renew.elements_balance()
    sleep(3600)
