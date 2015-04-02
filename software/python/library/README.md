Python PropellerHAT Code Uploader
=================================

Code uploader and Python bindings for the Propeller P8X32A Multi-core Microprocessor.

Uploader works as a standalone tool, run with:

    sudo python -m p1.loader

Credits
=======

Thanks to Remy Blank for the original code, released on the Parallax
forums in 2007. I have taken pains to credit him appropriately.

http://forums.parallax.com/showthread.php/90707-Propeller-development-for-non-Windows-users

Although I have changed the code quite significantly to fix performance
issues on the Raspberry Pi, and address GPIO reset, much of his work
remains in-tact and this code should be portable.

Thanks also to Jeff Martin who helped me understand the loader protocol
and whose improvements to the upload process I hope to implement soon.
