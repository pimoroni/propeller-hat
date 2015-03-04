#My First PASM

If you're anything like me, you'll see PASM ( Propeller Assembly ) as a looming challenge, begging to be tackled 
and surmounted whether or not it proves to be at all useful in your Pi projects.

Programmers can certainly succumb to "challenge accepted" moments, and PASM is one of those.

##Blink

Like all languages, the canonical way to get started is with a simple and easy blink example. Let's have a look
at one in PASM. What we'll actually see is a small SPIN program loading up a new Cog with the PASM we want to run.
All the code you run on a Propeller will start with a Cog running SPIN.

```spin
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
```

Whew! That's a lot to take in. While at first glance the PASM code may look like incomprehensible nonsense,
it's actually a lot easier to understand than it looks. Assembly doesn't have many of the constructs we take
for granted in most high level programming languages, and that means it doesn't have those complexities either.

Most of these Assembly commands are simply moving a number from one place to another, or performing an operation
upon two memory locations. Once you get a simple Blink program running, it becomes easier to experiment with how
other instructions affect, for example, your Pin value.

Onward to the explanation...

####cognew

You'll notice, if you've read through the Multicore tutorial, that our cognew command is ever so slightly different
this time around.

This is because PASM is wholly different to SPIN in how it operates, and is much more explicit about how memory is
used. SPIN needs a stack to store various snippets of information as it goes about its business, and what it stores
is completely hidden from the programmer, it's a high-level language.

PASM, on the other hand, only stores things where you tell it, when you tell it and how you tell it.

The second parameter in this instance becomes the read-only parameter passed into the new Cog. You can specify a
single number, a complicated 32-bits long bitfield, or just give it the memory address for a handful of parameters
stored in the Hub. This is all far too advanced for our first blink, though, so we'll stick with 0.

####DAT

All PASM is stored within the DAT section of its parent SPIN program. This is the easiest place to store PASM source
which everyone can see and modify, but it's not the only way. You could use an array of longs to store
compiled PASM instructions, or you could create PASM instructions on the fly ( please don't! for your own sanity! ).

####"org 0"

This is some PASM copypasta that you'll find at the top of most, if not all, blocks of PASM code in some form or 
another. It simply states that the following PASM code should start at Cog RAM addr 0.
