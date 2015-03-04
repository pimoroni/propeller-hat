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

```spin
DAT
```

All PASM is stored within the DAT section of its parent SPIN program. This is the easiest place to store PASM source
which everyone can see and modify, but it's not the only way. You could use an array of longs to store
compiled PASM instructions, or you could create PASM instructions on the fly ( please don't! for your own sanity! ).

```spin
org 0
```

This is some PASM copypasta that you'll find at the top of most, if not all, blocks of PASM code in some form or 
another. It simply states that the following PASM code should start at Cog RAM addr 0.

```spin
blink   mov     dira,   Pin
```

There's a lot going on in this line, but it's easy enough to break down.

The `blink` part is a label, this is a little note to the compiler telling it that we want to keep track of this
point in the program so we can find it later. This label can be passed into `cognew` to tell it where to locate our PASM. It can also be jumped to in PASM itself, you'll see this later.

Next comes the actual instruction: `mov dira, Pin`. The `mov` part is a simple mnemonic, a text name for a numerical
instruction that the Propeller can understand. If you hadn't guessed, it means "move" although it actually copies.

The rest of the instruction is made up of our destination, `dira` which is the address ( not the value ) of the
DIRA register, the very same one we use in SPIN. And, finally, the address of our source `Pin` which is a 32bit integer containing the pin mask we want to toggle.

So this instruction is telling the Propeller to `mov` the value of memory location `Pin` into register `dira`. Well,
 copy, since the Pin value remains unchanged.

Bear in mind that we're blatting the whole register by moving Pin into it, so our Pin will be the *only* output.

A far more appropriate instruction would be `or dira, Pin`, which would turn the Pin to an output if its not one,
and would otherwise leave it unchanged.

```spin
rdlong  Delay,  #0
```

Next up is a Hub access instruction. Propeller Assembly includes special instructions for accessing Hub memory.
This particular one, `rdlong`, reads a long ( a 32bit integer ) into its target from a source memory location.

In this instance `Delay` is our target, a long we've reserved for our use, and the source is `#0` which is a
*literal* memory address. So, we're loading Delay from Hub memory location 0. This just so happens to be where the
Propeller keeps the CLKFREQ value, which is the number of clock ticks in a second. Using this, we can create a 1sec
delay later.

```spin
mov     Time,   cnt
```

Just like our earlier `mov` instruction, we're copying the value of one memory address or register into another.

In this case we're priming `Time` with the value of the system counter, for which there's a handy shortcut `cnt`
so you don't have to remember its numeric memory location.

```spin
add     Time,   #9
```

Now for an `add` instruction. This one should be easy to understand. We're adding the literal value 9 ( we indicate
that it's not an address by prefixing with # ) to our Time variable.

But, why on earth are we doing this? The reason is perplexing, but simple once you understand it.

The `waitcnt` instruction in PASM will wait until the `cnt` register equals the value we give it. We're passing
it the value of `Time` for its first wait, if this value simply equalled the system counter then the very act of
calling `waitcnt`, which itself takes time, will cause us to miss the value we're looking for.

> Imagine I gave you a piece of paper with the number 30 on it, and told you at exactly 30 seconds past 
to wait until the clock next shows 30 seconds. By the time I've finished telling you what to do it's going to be
at least 32 seconds past- so you'll wait nearly a whole minute instead of the 30 seconds I wanted.

> When waitcnt misses a particular value of cnt, this is more or less what's happening!

A more succinct way to write this line would be:

```spin
add     Time,   Delay
```

Which causes our first `waitcnt` delay to be about 1 second, instead of the minimum possible delay. However I
deliberately left this minimum wait to illustrate a common tripping point in PASM.

```spin
:loop   waitcnt Time,   Delay
```

Now we start waiting. This line does two things.

* First `waitcnt` will wait until the system counter matches the value we've specified in `Time`.
* Second, the value of `Delay` will be added to `Time` to create the next value to wait for.

Because `Delay` is added to `Time` for us, there's no need to do it manually within the loop, and the next
time we call `waitcnt` in the same way, we'll handily get another 1 second delay.

This is, of course, unless all the things we've decided to do within the loop take more than the delay time!

The `:loop` prefix on this line is another label. Using ':' to prefix a label is a handy way of making it
obvious that it's a label, and not a variable, register address or instruction mnemonic. We've labelled this
line because, in order to loop, we want to jump back to it later.

The word "loop" is not required, you can make this label ":monkeys" if you want!

```spin
xor     outa,   Pin
```

This line is where the magic happens. We're finally setting a value to our output register `outa`.
Using `xor` is a *really* lazy way of toggling our output pin, since it literally means "exclusive or".

So, if our pin is on, we get:

`1 xor 1 = 0`

And if our pin is off, we get:

`0 xor 1 = 1`

And so on!

The thing to remember here is that xor is operating upon the whole 32bit register, so `xor` is a really handy
way to toggle a pin using a bit mask, without affecting the others.

