import os
import time

for count in range(1, 1000):
    os.system('python3 scripts/check-exchange.py -i domain.txt -o domaint.txt')
    time.sleep(60)
