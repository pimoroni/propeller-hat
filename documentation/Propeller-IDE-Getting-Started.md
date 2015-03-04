#Propeller IDE Getting Started

##Preface

Learning to program isn't just about mastering a particular programming language
and applying it in every situation. It's about learning the key concepts
and applying them to a wealth of different situations in many languages.

The phrase "If you've only got a hammer, everything looks like a nail," springs to mind.
Different circumstances often beg for, or even require, different programming languages.

**SPIN**

The native language of the Parallax Propeller is SPIN. Spin is a little Pythonic in nature, 
it uses spaces and indentation a syntax.

It also borrows a lot of syntax quirks from other languages, and thus isn't going to be
familiar from the get go. That's no problem, you'll master it in no time!

**Propeller IDE**

The weapon-of-choice software for writing Propeller SPIN is the Open-Source Propeller IDE.
It runs on the Raspberry Pi pretty well, and we've made sure you can upload code right onto
your Propeller HAT painlessly so you can get programming quickly and avoid the hassle of setting up.

The great thing about Propeller IDE, SPIN and the Propeller is that they're close-knit and
unencumbered by the need to support lots of different processors. This makes compiling and uploading
SPIN code absolutely lightning fast- Arduino users will be simply blown away.

##First Steps

###Installing Pre-requisites

Raspbian needs a little helping hand with some of Propeller IDE's dependencies, but hopefully a future
release will see the end of these steps.

First, add the following entries to `/etc/apt/sources.list`.

```
deb http://twolife.be/raspbian/ wheezy main backports
deb-src http://twolife.be/raspbian/ wheezy main backports
```

Add the repository key.

```bash
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key 2578B775
```

And finally update and install Qt5 and its dependencies, plus libftdi1 for the loader.

```bash
sudo apt-get update
sudo apt-get install qt5-default qt5-qmake libegl1-mesa libgles2-mesa libftdi1
```

###Installing Propeller IDE

Now, head over to [www.lamestation.com/propelleride/](http://www.lamestation.com/propelleride/) and grab the latest 
version of Propeller IDE for the Raspberry Pi.

![Propeller IDE download](images/propeller-ide-download.png)

It's easier if you grab the right URL, and use the wget command on your 
Raspberry Pi to download it. For example:

```bash
wget https://github.com/parallaxinc/PropellerIDE/releases/download/0.25.1/propelleride-0.25.1-0-g5442b03-armhf.deb
```

Once downloaded, you can install it with:

```bash
sudo dpkg -i propelleride-0.25.1-0-g5442b03-armhf.deb
```

###Turning off the Serial Terminal so you can talk to Propeller HAT

By default, the Raspberry Pi fires up a serial terminal on /dev/ttyAMA0. This is handy for debugging headless, but if you're using Propeller IDE and programming a Propeller HAT then you've likely got a monitor plugged in anyway!

The serial terminal must be disabled so that we can communicate with Propeller HAT. Fortunately, raspi-config makes this easy:

```bash
sudo raspi-config
```

Then navigate to Advanced Options, find the Serial option and disable it.

![Raspberry Pi, disable Serial Terminal](images/propeller-ide-serial-terminal.png)

###Making sure p1load can access your Raspberry Pi's GPIO pins

We need p1load to run as root, so it can access the GPIO pin used for resetting Propeller HAT. 

We've whipped up an install script that should get you started. 

First, you'll need to clone this repository if you haven't already:

```bash
git clone https://github.com/pimoroni/propeller-hat
```

Then cd to software/p1load and run ./install:

```bash
cd propeller-hat/software/p1load
./install
```

This will install the latest and greatest P1 Loader, bundled in this repo as a binary, and
make sure it has the right permissions to do its thing.

p1load defaults to using GPIO pin 17, pulled low when built for the Raspberry Pi, so this is all we need to do. You're good to go! Uploading code is as simple as:

```bash
p1load my-binary-file.binary
```

And to compile a SPIN file to a binary outside of the IDE, you can:

```bash
openspin my-spin-file.spin
```

#What next?

* [Your first SPIN program](/documentation/Your-first-SPIN-program.md)
