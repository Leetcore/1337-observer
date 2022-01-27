import os
import time
import colorama
colorama.init(autoreset=True)

os.system("clear")

def print_slow(color, input, speed):
    text_array = input.split("\n")
    for text in text_array:
        print(color + text)
        time.sleep(speed)

with open("groups/hosts.txt", "r") as myfile:
    fullscan = myfile.read()

print_slow("", fullscan, 0.1)