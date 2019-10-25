import blynklib
# import blynktimer
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
from datetime import datetime

BLYNK_AUTH = 'xxx'
# blynk = blynklib.Blynk(BLYNK_AUTH)

blynk = blynklib.Blynk(BLYNK_AUTH,
                       server='blynk-cloud.com',
                       port=8442,
                       heartbeat=60
                       )

# timer = blynktimer.Timer()

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)

GPIO.output(21, GPIO.LOW)
time.sleep(1)
GPIO.output(21, GPIO.HIGH)
time.sleep(1)
GPIO.output(21, GPIO.LOW)

dht11_sensor = Adafruit_DHT.DHT11

@blynk.handle_event('write V0')
def write_virtual_pin_handler(pin, value):
    # blynk.virtual_write(1, 1)
    if value[0] == '1':
        GPIO.output(21, GPIO.HIGH)
        print(1)
    else:
        GPIO.output(21, GPIO.LOW)
        print(0)


@blynk.handle_event('V2')
def write_temp_humid():
    humidity, temperature = Adafruit_DHT.read_retry(dht11_sensor, 4, retries=10, delay_seconds=10)
    if None not in (humidity, temperature):
        # print('{}: {:.1f} C, {:.1f} %'.format(datetime.now(), temperature, humidity))
        blynk.virtual_write(2, humidity)
        blynk.virtual_write(3, temperature)
    else:
        # blynk.virtual_write(2, 0)
        # blynk.virtual_write(3, 0)
        print('None error')


blynk.run()

while True:
    write_temp_humid()
