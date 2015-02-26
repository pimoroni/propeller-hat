#SIDPlay

This example uses SIDcog Serial Slave and a serial streamer written in C to stream raw SID register dumps
to Propeller HAT.

You will need to install wiringPi!

```bash
git clone git://git.drogon.net/wiringPi
cd wiringPi
./build
```

To upload the sid player, run:

    ./sidplay.py

To play a SID dump, run:

    ./sidplay SID_File [Frequenzy_HZ Duration_Sec]

To create a valid dump file you will need the SID dumper tool from here: http://forums.parallax.com/showthread.php/118285-SIDcog-The-sound-of-the-Commodore-64-!-%28Now-in-the-OBEX%29

