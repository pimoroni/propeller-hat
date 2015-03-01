#Diving Into Multicore

You probably didn't pick up Propeller HAT because it was some ordinary, run-of-the-mill Microcontroller board. No siree.
You want to take advantage of those 8 cores and play to the Propeller's strengths.

Well, fortunately, it's really not all that hard.

###What's a cog, got to do, got to do with it?

In the world of Propeller, where almost everything is a pun based on the name of the chip, you'll often find the cores
referred to as "cogs". The Propeller has 8 cogs, and ( wait for it... ) a "hub".

The Hub is the central controller of the Propeller, it houses the lion's share of the chips memory/storage - 8192, 32-bit
longs ( also known as 32kb or 32,768 bytes ). The Hub's job is to dish out tasks to the Cogs, control their access to its
memory and make sure they don't fight over resources or tread on each other's toes.

In other words, the Hub is the boss! What it doesn't have, however, is the ability to run code. The Hub sits in its tiny
silicon throne and dishes out commands, but it can't execute any itself. The Hub relies wholly and totally on the Cogs to carry
out their instructions and only gets involved when they need to communicate, share data or receive new sets of instructions.

The Hub also has some other fancy features, such as configuration registers and lock bits- we won't worry about those yet!

Now. Onto the Cogs. Each Cog has 512, 32-bit longs ( also known as 2kb or 2048 bytes ) of memory. This memory serves as both
storage for the instuctions that Cog has been told to execute, and as running memory for remembering what it's doing.

2kb is a pretty decent amount of memory for a Cog, but you have to be mindful that the larger your running code is, the less
space will be available for it to store what it's working on. Think of it like filling a frying pan- the more food you pop
into the frying pan the less space you have to stir it!

Alongside the memory, each Cog has its own CPU capable of executing the instructions its given, it also has its own
counters and video generator- but we'll worry about those later too.

The most important thing to remember is that each one of the 8 Cogs has its own DIRA and OUTA register for setting the
direction and output state of all 32 IO pins on the Propeller. When you're passing a function or code to a Cog you need
to make sure that the Cog sets up its own DIRA register, since setting the direction of a pin elsewhere will likely happen
in another Cog and lead to confusing results!

###Now, for some code!
