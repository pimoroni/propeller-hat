#Propeller HAT Documentation

Ahoy! If you're reading this, you're probably the proud over of a shiny new Propeller HAT.
If so, thanks for picking one up, and I hope you enjoy discovering the quirks of this
powerful little Micro Controller as much as I did.

##Propeller IO Quick Start

The Propeller HAT Python library includes a set of IO modules which, when loaded, automatically
flash your Propeller HAT with firmware to handle things like PWM and basic Input/Output.

The best way to explorer these is to install the Propeller HAT library and run one of them:

```bash
sudo pip install p1
sudo python -im p1.pwm
```

This loads p1.pwm, a PWM library for Propeller HAT which gives you 30 software PWM pins handled
by the Propeller itself and uninterrupted by anything you might do on the Pi.
