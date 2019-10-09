from flask import Flask, render_template, Response
# from flask_ngrok import run_with_ngrok
import subprocess
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import time
from datetime import datetime
import time
from picamera import PiCamera
import random
import io
import os


app = Flask(__name__, static_folder='/home/pi/RPI/templates')
# run_with_ngrok(app)

temp_history = []

def now():
    ts = time.time()
    date_and_time = datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
    return date_and_time

def date():
    ts = time.time()
    date = datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    return date

def generate_id():
    return random.randint(1, 100000)

def check_cpu():
    o = subprocess.Popen(["vcgencmd",  "measure_temp"], stdout=subprocess.PIPE)
    (output, err) = o.communicate()
    output = output.decode()
    cpu_temp = int(output.replace('temp=', '').replace('.0\'C', ''))
    temp_history.append(cpu_temp)
    return cpu_temp

def show_cpu_temp_history():
    plt.plot(temp_history)
    plt.ylabel('CPU temperature (C)')
    plt.xlabel('time')
    plt.savefig('/home/pi/RPI/templates/cpu_temp_plot.jpg')
    return None

@app.route("/")
@app.route('/index')
def index():
    today = date()
    id = generate_id()
    return render_template('index.html', cpu_temp=check_cpu(), cpu_temp_history=show_cpu_temp_history(), id=id, today=today)

@app.route('/camera')
def camera():
    camera = PiCamera()
    camera.rotation = 180
    camera.resolution = (800, 600)
    camera.framerate = 30
    # camera.contrast = 80

    camera.start_preview()
    time.sleep(1) # warming up
    date_and_time = now()
    camera.capture('/home/pi/RPI/templates/photos/photo_{}.jpg'.format(date_and_time))
    camera.stop_preview()
    camera.close()
    return render_template('photo_gallery.html', date_and_time=date_and_time)

@app.route('/loop_camera')
def loop_camera():
    camera = PiCamera()
    camera.rotation = 180
    camera.resolution = (800, 600)
    camera.framerate = 30
    # camera.contrast = 80

    today = date()
    directory_path = '/home/pi/RPI/templates/loop_photos/{}'.format(today)

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    camera.start_preview()
    for i in range(60):
        time.sleep(1) # warming up / time to save file
        camera.capture('/home/pi/RPI/templates/loop_photos/{}/loop_photo_{}.jpg'.format(today, i))
    camera.stop_preview()
    camera.close()
    return render_template('photo_gallery.html')

@app.route('/photo_gallery')
def photo_gallery():
    return render_template('photo_gallery.html')

def main():
    app.run(host='127.0.0.1', port=80, debug=True)
    
if __name__ == '__main__':
    main()
