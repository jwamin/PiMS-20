# Pi-MS-20

## Experimentations and tooling into driving Korg MS-20 Semi-modular synth with Raspberry Pi GPIO using minimal additional components

### Outline

#### Control Voltages

* You'd need a DAC to generate control voltages using RPi GPIO.

#### Pulse Width Modulation (PWM)

* Raspberry PI Hardware-based PWM's 0-3v3 can be used standalone as:
    * External Signal Source
    * LFO

* In conjunction with the MS20's external signal processor (ESP) F-C Converter Patch connector to output control voltages

### TODO

* argparse
* OO 
* API

### Next Steps

* PWM improvements - easing, interesting sounds, better control, "one shot" sounds. 
* frameworkize
* keyboard control
* midi notes to pwm frequency?

Reference

https://github.com/Pioreactor/rpi_hardware_pwm  
