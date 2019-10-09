# import subprocess

# subprocess.call(["vcgencmd",  "measure_temp"])
# subprocess.call("date")


import time
from datetime import datetime

ts = time.time()
now = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
print(now)
