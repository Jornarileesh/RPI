import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import pandas as pd

dht11_sensor = Adafruit_DHT.DHT11

hum_values = []
temp_values = []
dump_limit = 3600

def get_temp_humid():
    humidity, temperature = Adafruit_DHT.read_retry(dht11_sensor, 4, retries=10, delay_seconds=60)
    if None not in (humidity, temperature):
        hum_values.append(humidity)
        temp_values.append(temperature)
    else:
        print('None error')


def check_data_dump():
    hum_len = len(hum_values)
    temp_len = len(temp_values)
    
    if hum_len == dump_limit:
        assert
        # save to file using pandas or simpler to csv
        # clear table
    if temp_len == dump_limit:
        assert
        # save to file using pandas or simpler to csv
        # clear table


while True:
    get_temp_humid()
