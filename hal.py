import sys
import os
import subprocess
import datetime
# import pigpio
import datetime
import json
import time
import requests
import RPi.GPIO as GPIO

from time import sleep

from auth import Token
import blynklib

blynk = blynklib.Blynk(Token.BlynkHal)

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.OUT)
ServoH = GPIO.PWM(18, 50)
GPIO.setup(12, GPIO.OUT)
ServoV = GPIO.PWM(12, 50)

ServoH.stop()
ServoV.stop()

photoNameTemp = "#"
photoIndex = 0
port = 0
ss_value = ''
ss_index = ''
iso_value = ''
ev_value = ''
awb_value = ''
default = True

ss_table = [
    ['auto', ''],
    ['30', '30000000'],
    ['15', '15000000'],
    ['8', '8000000'],
    ['4', '4000000'],
    ['2', '2000000'],
    ['1', '1000000'],
    ['1/2', '500000'],
    ['1/4', '250000'],
    ['1/8', '125000'],
    ['1/15', '66666'],
    ['1/30', '33333'],
    ['1/60', '16666'],
    ['1/125', '8000'],
    ['1/250', '4000'],
    ['1/500', '2000'],
    ['1/1000', '1000'],
    ['1/2000', '500'],
    ['1/4000', '250'],
    ['1/8000', '125'],
    ['1/50000', '20'],
    ['1/1000000', '1'],
]

port_table = [
    ['port: 80', '80'],
    ['port: 8160', '8160']
]


def takePhoto():
    photoSavePath = '/var/www/html/photos/'
    Date = datetime.datetime.now().strftime("%d-%m-%y_%H-%M-%S")
    photoName = Date + '.jpg'

    print(ss_value)

    comm = ['raspistill', '-w', '3280', '-h', '2464', '-ss', ss_value, '-ISO', iso_value, '-ev', ev_value, '-awb',
            awb_value, '-o', photoSavePath + photoName]
    subprocess.Popen(comm)
    return photoName


def run(process):
    comm = 'whoami'

    if process == 'http':
        blynk.virtual_write(11, port_table[port][0])
        comm = ['nohup', '/home/pi/ngrok', 'http', port_table[port][1]]
    elif process == 'stream':
        comm = ['nohup', '/usr/vlc-wrapper/stream.sh']
    else:
        comm = process
    subprocess.Popen(comm)


def kill(process):
    comm = ['pkill', process]
    subprocess.Popen(comm)


# def get_ngrok_url():
#     url = "http://localhost:4040/api/tunnels/"
#     try:
#         res = requests.get(url)
#         res_unicode = res.content.decode("utf-8")
#         res_json = json.loads(res_unicode)
#         for i in res_json["tunnels"]:
#             if i['name'] == 'command_line':
#                 return i['public_url']
#                 break
#     except requests.ConnectionError, e:
#         return 'ngrokErr'


# def addPhoto(photoName):
#     global photoIndex
#     photoIndex = photoIndex + 1
#     photoUrl = get_ngrok_url() + '/photos/' + photoName
#     blynk.virtual_write(11, photoName)
#     blynk.set_property(12, 'urls', photoUrl)
#
#     print(photoUrl)
#     blynk.virtual_write(12, photoIndex)


def photoMonitor():
    output = 'SS: ' + ss_index + ' ISO: ' + iso_value + ' EV: ' + ev_value
    blynk.virtual_write(15, output)


# run http server
@blynk.handle_event('write V0')
def write_virtual_pin_handler(pin, value):
    if value[0] == '1':
        run('http')
    else:
        kill('ngrok')

    # run stream process


@blynk.handle_event('write V1')
def write_virtual_pin_handler(pin, value):
    if value[0] == '1':
        run('stream')
    else:
        kill('raspivid')
        kill('vlc')

    # get ngrok url


@blynk.handle_event('write V2')
def write_virtual_pin_handler(pin, value):
    ngrok_url = get_ngrok_url()
    print(ngrok_url)
    blynk.virtual_write(11, ngrok_url)
    blynk.set_property(10, 'url', ngrok_url)


# take photo
@blynk.handle_event('write V3')
def write_virtual_pin_handler(pin, value):
    global photoNameTemp
    if value[0] == '1':
        photoNameTemp = takePhoto()
    else:
        addPhoto(photoNameTemp)


# joystick control
@blynk.handle_event('write V4')
def write_virtual_pin_handler(pin, value):
    value[0] = int(value[0])
    value[1] = int(value[1])

    dc = [7.5, 5.5]

    if (value[0] == 0):
        blynk.virtual_write(11, value[0])
        ServoH.stop()
    else:
        ServoH.start(dc[0] + value[0] / 10)
        # ServoV.start(dc[0] + value[1] / 10)


# port select
@blynk.handle_event('write V13')
def write_virtual_pin_handler(pin, value):
    global port
    port = int(value[0])
    blynk.virtual_write(11, port_table[port][0])


# shutter speed
@blynk.handle_event('write V14')
def write_virtual_pin_handler(pin, value):
    slider_pos = int(value[0])
    global ss_value
    ss_value = ss_table[slider_pos][1]
    global ss_index
    ss_index = ss_table[slider_pos][0]
    photoMonitor()


# iso
@blynk.handle_event('write V16')
def write_virtual_pin_handler(pin, value):
    global iso_value
    iso_value = value[0]
    photoMonitor()


# ev
@blynk.handle_event('write V17')
def write_virtual_pin_handler(pin, value):
    global ev_value
    ev_value = value[0]
    photoMonitor()


@blynk.handle_event('write V18')
def write_virtual_pin_handler(pin, value):
    global awb_value
    awb_value = value[0]


def defaultSettings():
    blynk.virtual_write(17, 0)
    photoMonitor()


try:
    while True:
        blynk.run()
        if default:
            defaultSettings()
        default = False

finally:
    GPIO.cleanup()
    print('cleanup')
