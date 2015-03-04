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

The value for requency is calculated like so: 1/<Desired Frequency> * 1000 * 1000

So if you want 50Hz, it's 1/50 * 1000 * 1000, or 20,000, eg: `p1.pwm.duty(0, 50, 20000)`.

```python
p1.pwm.pulse(pin,on_time,off_time)
```

Pulse a pin with on_time on duration and off_time off duration. Pulse accepts values between 0 and 65535.

The On and Off times are measured in units of 8.2us, giving a range of 0 to 537,387 ( or about 0.53 sec )<sup>1</sup>.

For example `p1.pwm.pulse(0,60975,60975)` is the closest you can get to toggling a pin every 0.5sec.

```python
p1.pwm.servo(pin, pulse)
```

Drive a servo with a specific pulse width in nanoseconds.
Look up your servo datasheet to see what pulse width corresponds to your desired angle.


####Notes

* <sup>1</sup> I may expand this to a 3-byte integer ranging from 0 to 16,777,215, or 0 to 137sec, but since
the Pi is fine at long pulse intervals it wouldn't be much use!

