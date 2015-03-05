CON
  _CLKMODE = xtal1 + pll16x
  _XINFREQ = 6_000_000

  MY_LED_PIN = 0

PUB main
  cognew(@blink, 0) ' Start a Cog with our assembly routine, no stack 
                    ' is required since PASM requires we explicitly 
                    ' assign and use memory locations within the Cog/Hub
DAT
        org     0
blink   mov     dira,   Pin       ' Set our Pin to an output
        rdlong  Delay,  #0        ' Prime the Delay variable with memory location 0
                                  ' this is where the Propeller stores the CLKFREQ variable
                                  ' which is the number of clock ticks per second
        mov     Time,   cnt       ' Prime our timer with the current value of the system counter
        add     Time,   #9        ' Add a minimum delay ( more on this below )
:loop   waitcnt Time,   Delay     ' Start waiting
        xor     outa,   Pin       ' Toggle our output pin with "xor"
        jmp     #:loop            ' Jump back to the beginning of our loop

Pin     long    |< MY_LED_PIN     ' Encde MY_LED_PIN to a bit mask
Delay           res     1
Time            res     1
        fit
