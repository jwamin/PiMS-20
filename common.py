from rpi_hardware_pwm import HardwarePWM
from easing_functions import *
from pitchtools import n2f
from time import sleep
from typing import Callable
import enum
import logging
from os import environ

PWM_CHANNEL = 0
PWM_CHIP = 0
PWM_FREQUENCY = 100 #hz
PWM_DEFAULT_DUTY = 50 #square pulse
PWM_DEFAULT_MOD_FREQUENCY = 50 #hz

PWM_LOW_DUTY = environ.get("PWM_LOW_DUTY") or 0
PWM_HIGH_DUTY = environ.get("PWM_HIGH_DUTY") or 100

FPS_60 = 1 / 60
FPS_120 = 1 / 120

logging_level = logging.basicConfig(level=logging.DEBUG)
logger = logging

class Easing(enum.Enum):
    linear: Callable = LinearInOut
    inout: Callable = QuinticEaseInOut

def uline_print(str:str, character:chr = "="):
    length = len(str)
    print(f"{str}\n{character*length}")


def start_pwm(freq:float, duty: float, cycle: bool, rise_and_fall: bool):
    try: 
        pwm = HardwarePWM(pwm_channel=PWM_CHANNEL, hz=freq, chip=PWM_CHIP)
        pwm.start(duty) # full duty cycle

        if cycle:
            duty_min = 0.1
            duty_max = 100
            current_duty = duty_min
            cycle_freq = cycle 
            step = cycle_freq / freq
            rising = rise_and_fall
            cycle_step = 1 / cycle_freq
            logger.debug(f"cycle freq: {cycle_freq}, step: {step}, cycle_step: {cycle_step}")
            while(True):
                pwm.change_duty_cycle(current_duty)
                sleep(cycle_step)
                logger.debug(current_duty)
                if rise_and_fall:
                    if rising:
                        current_duty = min(current_duty + step,duty_max)
                    else:
                        current_duty = max(current_duty - step,duty_min)
                    if rise_and_fall:
                        if current_duty >= duty_max and rising:
                            rising = False
                        elif current_duty <= duty_min and not rising:
                            rising = True
                else:
                    current_duty = min(current_duty + step, duty_max) if current_duty < duty_max else 0 
        else:
            while(True):
                sleep(1)
    except KeyboardInterrupt as kbi:
        print("\n")
        pwm.stop()

def pwm_easing(easingFunction:Callable = QuinticEaseInOut,
               frequency:float = PWM_FREQUENCY,
               width_mod_frequency:float = PWM_DEFAULT_MOD_FREQUENCY,
               min_duty:int = PWM_LOW_DUTY,
               max_duty:int = PWM_HIGH_DUTY):

    try:
        # Start PWM
        pwm = HardwarePWM(pwm_channel=PWM_CHANNEL, hz=frequency, chip=PWM_CHIP)
        pwm.start(min_duty)

        one_cycle = 1 / width_mod_frequency
        duration = one_cycle

        ease = easingFunction(min_duty,
                              max_duty,
                              duration)

        update_time = duration / 60 

        #
        # modulation frequency = x times a second
        # duration of 1 cycle at modulation frequency = 1 / x
        # update_time = duration / arbitrary fraction
        #

        logger.debug(f"starting easing pwm with{easingFunction}")
        logger.debug(f"easing min: {min_duty}, max: {max_duty} duration: {duration}")
        logger.debug(f"frequency: {frequency}, modulation frequency: {width_mod_frequency}")
        logger.debug(f"once-cycle: {one_cycle}, 60FPS: {FPS_60} updateTime: {update_time}\n\n")

        startTime = 0
        currentTime = startTime

        while(True):
            while currentTime <= max_duty:
                try:
                    newduty = ease(currentTime)
                    logger.debug(f"{newduty}, {currentTime}")
                    pwm.change_duty_cycle(newduty)
                    newTime = currentTime + update_time
                    currentTime = newTime if newTime <= duration else startTime
                    logger.debug(f"next will be {currentTime}, {newTime} {max_duty >= newTime >= min_duty}- sleeping for {one_cycle} {FPS_60} {FPS_120}")
                    sleep(update_time)
                except Exception as e:
                    logger.error(e)
                    logger.debug(f"tried to set new duty of: {newduty} - currentTime {currentTime} - max-duty: {max_duty} - min-duty {min_duty}")
                    pwm.stop()
                    exit(1)
            logger.debug("restarting")
            currentTime = 0
    except KeyboardInterrupt as kbi:
        print("\n")
        pwm.stop()


def pulse_frequency_mod_easing(easingFunction:Callable = LinearInOut, note_start = "C2", note_end = "C3", start_time = 1, duration = 5, hold_time = 3):

    try:

        start_freq = n2f(note_start)
        end_freq = n2f(note_end)

        # Start PWM
        pwm = HardwarePWM(pwm_channel=PWM_CHANNEL, hz=start_freq, chip=PWM_CHIP)
        pwm.start(PWM_DEFAULT_DUTY)

        sleep(start_time)

        easing = easingFunction(start_freq,end_freq,duration)

        currentTime = 0

        while currentTime < duration:
            value = easing(currentTime)
            pwm.change_frequency(value)
            next = currentTime + FPS_60
            currentTime = next 
            sleep(FPS_60)

        sleep(hold_time)

        pwm.stop()

    except KeyboardInterrupt as kbd:
        logger.error(f"keyboard interrupt {kbd}")
        pwm.stop()
    except Exception as e:
        logger.error(f"some other exception {e}")
        pwm.stop()