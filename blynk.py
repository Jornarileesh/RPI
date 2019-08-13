import blynklib
import RPi.GPIO as GPIO


BLYNK_AUTH = 'tLQHdWKu8j0ZyQ_C0H1L1nUVsWI5iKA8'
# base lib init
blynk = blynklib.Blynk(BLYNK_AUTH)

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
turn_off_light():


def turn_on_light():
    GPIO.output(21, GPIO.HIGH)


def turn_off_light():
    GPIO.output(21, GPIO.LOW)


@blynk.handle_event('write GP21')
def write_virtual_pin_handler(pin, value):
    if value == 1:
        blynk.virtual_write(21, 1)
        # turn_on_light()
    elif value == 0:
        blynk.virtual_write(21, 0)
        # turn_off_light()


while True:
    blynk.run()

# dioda - pin 40 (GPIO21)
# masa pin 39
