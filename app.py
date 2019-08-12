from flask import Flask, render_template
# from flask_ngrok import run_with_ngrok
import subprocess
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import time

app = Flask(__name__, static_folder='/home/pi/webserver/templates')
# run_with_ngrok(app)

temp_history = []
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.HIGH)
time.sleep(3)
GPIO.output(21, GPIO.LOW)


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
    plt.savefig('templates/cpu_temp_plot.jpg')


def turn_on_light():
    GPIO.output(21, GPIO.HIGH)


def turn_off_light():
    GPIO.output(21, GPIO.LOW)


@app.route("/")
@app.route('/index')
def index():
    return render_template('index.html', cpu_temp=check_cpu(), cpu_temp_history=show_cpu_temp_history())


@app.route('/', methods=['GET', 'POST'])
def leds():
    form = SentiForm()
    if form.is_submitted():
        flash('Prediction: {}'.format(
            sentiment_prediction(form.text.data, model)))
        return redirect('/index')
    return render_template('sentiment-analysis.html', form=form)


def main():
    app.run(host='127.0.0.1', port=80, debug=True)


if __name__ == '__main__':
    main()
