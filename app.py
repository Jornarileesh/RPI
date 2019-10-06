from flask import Flask, render_template, Response
# from flask_ngrok import run_with_ngrok
import subprocess
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import time
from datetime import datetime
from picamera import PiCamera
import random
from camera_pi import Camera
import io


app = Flask(__name__, static_folder='/home/pi/RPI/templates')
# run_with_ngrok(app)

temp_history = []


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

def turn_on_light():
    return None

@app.route("/")
@app.route('/index')
def index():
    id = random.randint(1, 10000)
    return render_template('index.html', cpu_temp=check_cpu(), cpu_temp_history=show_cpu_temp_history(), id=id)

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

@app.route('/video')
def video():
    # camera = PiCamera()
    # camera.start_preview()
    # camera.start_recording('/home/pi/RPI/templates/video.mjpeg')
    # time.sleep(10)
    # camera.stop_recording()
    # camera.stop_preview()
    # camera.close()
    return render_template('video.html')

@app.route('/photo_gallery')
def photo_gallery():
    id = random.randint(1, 10000)
    return render_template('photo_gallery.html', id=id)

@app.route('/video_gallery')
def video_gallery():
    id = random.randint(1, 10000)
    return render_template('video_gallery.html', id=id)

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(video_stream()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def video_stream():
    with PiCamera() as camera:
        stream = io.BytesIO()
        for foo in camera.capture_continuous(stream, format='jpeg'):
            # Truncate the stream to the current position (in case
            # prior iterations output a longer image)
            stream.truncate()
            stream.seek(0)

def main():
    app.run(host='127.0.0.1', port=80, debug=True)
    
if __name__ == '__main__':
    main()
