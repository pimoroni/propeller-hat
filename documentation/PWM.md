#Propeller HAT PWM

Propeller HAT PWM is a Python library which flashes your Propeller HAT with a 30-pin
PWM driver library for controlling LEDs or servos.

It lets you drive 30 pins from A0 to A29, outputting PWM pulses, duty cycles or servo
commands with a simple serial protocol.

##Prerequisites

Propeller HAT PWM communicates over serial, so you don't need any extra wiring.

##Library Reference

```python
p1.pwm.duty(pin, duty, freq)
```

PWM the pin with a duty cycle of duty ( 0 to 100% ) at the defined frequency.

```python
p1.pwm.pulse(pin,on_time,off_time)
```

Pulse a pin with on_time on duration and off_time off duration. Easy blinking LEDs!

```python
p1.pwm.servo(pin, pulse)
```

Drive a servo with a specific pulse width in nanoseconds.
Look up your servo datasheet to see what pulse width corresponds to your desired angle.

