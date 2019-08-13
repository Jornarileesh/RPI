import blynklib
import RPi.GPIO as GPIO


BLYNK_AUTH = 'tLQHdWKu8j0ZyQ_C0H1L1nUVsWI5iKA8'
# base lib init
blynk = blynklib.Blynk(BLYNK_AUTH)

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)


def turn_on_light():
    GPIO.output(21, GPIO.HIGH)


def turn_off_light():
    GPIO.output(21, GPIO.LOW)


@blynk.handle_event('read GP21')
def read_virtual_pin_handler():
    blynk.virtual_write(1, 1)
    turn_on_light()


while True:
    blynk.run()


# dioda - pin 40 (GPIO21)
# masa pin 39
