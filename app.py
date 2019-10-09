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


app = Flask(__name__, static_folder='/home/pi/RPI/templates')
# run_with_ngrok(app)

temp_history = []
ts = time.time()
now = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


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
    id = random.randint(1, 10000)
    return render_template('index.html', cpu_temp=check_cpu(), cpu_temp_history=show_cpu_temp_history(), id=id, date=now)

@app.route('/camera')
def camera():
    camera = PiCamera()
    camera.rotation = 180
    camera.resolution = (800, 600)
    camera.framerate = 30
    # camera.contrast = 80

    camera.start_preview()
    time.sleep(1)
    camera.capture('/home/pi/RPI/templates/photo.jpg')
    camera.stop_preview()
    camera.close()
    return render_template('camera.html')

@app.route('/loop_camera')
def loop_camera():
    camera = PiCamera()
    camera.rotation = 180
    camera.resolution = (800, 600)
    camera.framerate = 30
    # camera.contrast = 80

    camera.start_preview()
    time.sleep(1)
    camera.capture('/home/pi/RPI/templates/photo.jpg')
    camera.stop_preview()
    camera.close()
    return render_template('camera.html')

@app.route('/photo_gallery')
def photo_gallery():
    id = random.randint(1, 10000)
    return render_template('photo_gallery.html', id=id)

def main():
    app.run(host='127.0.0.1', port=80, debug=True)
    
if __name__ == '__main__':
    main()
