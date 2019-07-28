import subprocess

subprocess.call(["vcgencmd",  "measure_temp"])
# subprocess.call("date")