#!/usr/bin/python3
from sys import argv
import argparse
from common import uline_print, start_pwm, PWM_CHANNEL, PWM_CHIP, PWM_DEFAULT_DUTY,PWM_FREQUENCY

print("\n")
uline_print("Hardware PWM Test Tool")
print("Pins are configured in /boot/config.txt on your RPi")

print(f"channel {PWM_CHANNEL}, pin 13, chip {PWM_CHIP}")
print("Keyboard interrupt with Ctrl-C to stop Pulse")
default_freq = PWM_FREQUENCY 
default_duty = PWM_DEFAULT_DUTY
cycle = False
rise_and_fall = False

#print(argv)

#refactor to argparse
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("--frequency", type=float, default=default_freq, help="The frequency in hz of pwm signal", dest="freq")
parser.add_argument("--duty", type=float, default=default_duty, help="The duty of pwm signal", dest="duty")
parser.add_argument("--cycle", type=int, default=cycle, help="should cycle duty", dest="cycle")
parser.add_argument("--rise_and_fall", type=int, default=rise_and_fall, help="cycle should rise and fall", dest="rise")

args = parser.parse_args()
print(args)

freq:float = args.freq
duty:float = args.duty
cycle = bool(args.cycle)
rise_and_fall = bool(args.rise)

print(f"freq: {freq}, initial duty: {duty} cycle: {cycle} rise_and fall: {rise_and_fall}")

start_pwm(freq,duty,cycle,rise_and_fall)


