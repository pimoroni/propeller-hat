#!/usr/bin/env python

"""Parallax Propeller code uploader
Copyright (C) 2007 Remy Blank

This file is part of PropTools.

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, version 2. 

License: http://www.gnu.org/licenses/gpl-2.0.html

This program is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General 
Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

Modified January 2015 by Phil Howard <phil@pimoroni.com>
Modifications include support for the Raspberry Pi, mainly a
GPIO-based reset mechanism for GPIO-connected Propeller boards.

Various tweaks to the code have also been made both for general clarity
and to bring it closer to the Python PEP 8 style guidelines.

I have also extensively commented appropriate areas and attempted
to explain in sufficient detail the workings of the protocol.
"""

import glob
import os
import sys
import time

try:
    import serial
except ImportError:
    sys.exit("This library requires the serial module\nInstall with: sudo pip install pyserial")


# Processor constants
LFSR_REQUEST_LEN   = 250
LFSR_REPLY_LEN     = 250
LFSR_SEED          = ord("P")
CMD_SHUTDOWN       = 0
CMD_LOADRAMRUN     = 1
CMD_LOADEPPROM     = 2
CMD_LOADEPPROMRUN  = 3
EEPROM_SIZE        = 32768

# Platform defaults
defSerial = {
    "posix": "/dev/ttyUSB0",
    "nt": "COM1",
}

class LoaderError(Exception): pass

def do_nothing(msg):
    """Do nothing progress callback."""
    pass

def serial_ports():
    """Lists serial ports

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of available serial ports

    From: http://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
    """
    if sys.platform.startswith('win'):
        ports = ['COM' + str(i + 1) for i in range(256)]

    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this is to exclude your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')

    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')

    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

class Loader(object):
    """Propeller code uploader."""
    
    def __init__(self, port, reset_gpio=-1):
        self.serial = serial.Serial(baudrate=115200, timeout=0)
        self.serial.port = port
        self.reset_gpio = reset_gpio
        self.gpio = None

        if self.reset_gpio > -1:
            try:
                import RPi.GPIO as GPIO
                self.GPIO = GPIO
                self.GPIO.setmode(self.GPIO.BCM)
                self.GPIO.setwarnings(False)
                self.GPIO.setup(self.reset_gpio, self.GPIO.OUT, initial=self.GPIO.HIGH)
            except ImportError:
                print("RPi.GPIO library required for GPIO reset.")

    def _cleanup(self):
        if self.serial.isOpen():
            self.serial.close()

        if self.reset_gpio > -1 and not self.GPIO == None:
            self.GPIO.cleanup()

    def __del__(self):
        self._cleanup()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self._cleanup()
        
    def _lfsr(self, seed):
        """Generate bits from 8-bit LFSR with taps at 0xB2."""
        while True:
            yield seed & 0x01
            seed = ((seed << 1) & 0xfe) | (((seed >> 7) ^ (seed >> 5) ^ (seed >> 4) ^ (seed >> 1)) & 1)

    # High-level functions
    def get_version(self, progress=do_nothing):
        """Connect to the Propeller and return its version."""
        self._open()
        try:
            version = self._connect()
            self._write_long(CMD_SHUTDOWN)
            time.sleep(0.010)
            self.reset()
            return version
        finally:
            self._close()
        
    def upload(self, code=None, path=None, eeprom=False, run=True, progress=do_nothing, terminal=False):
        """Connect to the Propeller and upload code to RAM or EEPROM."""
        if path is not None:
            f = open(path, "rb")
            try:
                code = f.read()
            finally:
                f.close() 
        self._open()
        try:
            code, code_len = self._prepare_code(code, eeprom)
            version = self._connect()
            progress("Connected (version={})".format(version))
            self._send_code(code, code_len, eeprom, run, progress)
        finally:
            if terminal:
                while True:
                    ser = self.serial.read()
                    if ser != None:
                        sys.stdout.write(ser)
                        sys.stdout.flush()
            else:
                self._close()
    
    # Low-level functions
    def _open(self):
        try:
            self.serial.open()
        except OSError as e:
            raise LoaderError(str(e))
    
    def _close(self):
        self.serial.close()
        
    def reset(self):
        """Reset the Propeller

        Will use GPIO if a GPIO pin is specified
        """
        self.serial.flushOutput()

        if self.reset_gpio > -1 and not self.GPIO == None:
            self.GPIO.output(self.reset_gpio, self.GPIO.LOW)
            time.sleep(0.025)
        self.GPIO.output(self.reset_gpio, self.GPIO.HIGH)
            time.sleep(0.090)
        else:
            self.serial.setDTR(1)
            time.sleep(0.025)
            self.serial.setDTR(0)
            time.sleep(0.090)

        self.serial.flushInput()
        
    def _calibrate(self):

        """Send calibration pulse to the Propeller

        This exploits the start bit in the RS232 Serial protocol
        which counts as one single pulse.

        0xf9 = 0b11111001

        So the actual pulse sent is ( LSB first ):

        _-__-----
        010011111

        Which is a single t ( one ) pulse followed by a
        2t ( two ) pulse in Propeller speak.

        This calibrates a single bit of the serial transmission as "t"
        and by using either 0xff ( 255 ) or 0xfe ( 254 ) we can send
        either a 1 ( t ) or 0 ( 2t ) like so:

        0xff = 0b11111111
        _--------
        011111111

        or

        0xfe = 0b11111110
        __-------
        001111111

        The amount of time between pulses, as long as it is less than 100ms,
        is irrelevant so the bits can be packed closer by clever manipulation
        of the serial protocol ( which probably wont happen here! )

        """
        self._write_byte(0xf9)
        
    def _connect(self):
        """Connect to the Propeller and send/receieve the 250 bit
        LFSR handshake and 250 bit response.
        """
        self.reset()
        self._calibrate()
        seq = []
    
        # Prime the LFSR sequence with 500 values. LFSR wraps at 256
        for (i, value) in zip(range(LFSR_REQUEST_LEN + LFSR_REPLY_LEN), self._lfsr(LFSR_SEED)):
            seq.append(value)

        # Send the first 250 values from the LFSR
        self.serial.write("".join(chr(each | 0xfe) for each in seq[0:LFSR_REQUEST_LEN]))
    
        # Send 258 templates to "clock" the return values back to us
        # These are 250 bits of LFSR respone, plus
        # 8 bits denoting the Propeller version
        self.serial.write(chr(0xf9) * (LFSR_REPLY_LEN + 8))

        # Prop will return the last 6 values of the LFSR and then wrap
        # returning 244 additional values
        for i in range(LFSR_REQUEST_LEN, LFSR_REQUEST_LEN + LFSR_REPLY_LEN):
            if self._read_bit(False, 0.100) != seq[i]:
                raise LoaderError("No hardware found")

        # Prop will return 8 bits denoting the Propeller version
        version = 0
        for i in range(8):
            version = ((version >> 1) & 0x7f) | ((self._read_bit(False, 0.050) << 7))
        return version

    def _bin_to_eeprom(self, code):
        if len(code) > EEPROM_SIZE - 8:
            raise LoaderError("Code too long for EEPROM (max %d bytes)" % (EEPROM_SIZE - 8))
        dbase = ord(code[0x0a]) + (ord(code[0x0b]) << 8)
        if dbase > EEPROM_SIZE:
            raise LoaderError("Invalid binary format")
        code += "".join(chr(0x00) * (dbase - 8 - len(code)))
        code += "".join(chr(each) for each in [0xff, 0xff, 0xf9, 0xff, 0xff, 0xff, 0xf9, 0xff])
        code += "".join(chr(0x00) * (EEPROM_SIZE - len(code)))
        return code

    def _prepare_code(self, code, eeprom=False):
        if len(code) == 0:
            raise LoaderError("Empty file specified")

        if len(code) % 4 != 0:
            raise LoaderError("Invalid code size: must be a multiple of 4")

        if eeprom and len(code) < EEPROM_SIZE:
            code = self._bin_to_eeprom(code)

        checksum = reduce(lambda a, b: a + b, (ord(each) for each in code))

        if not eeprom:
            checksum += 2 * (0xff + 0xff + 0xf9 + 0xff)

        checksum &= 0xff

        if checksum != 0:
            raise LoaderError("Code checksum error: 0x{:0>2x}".format(checksum))

        code_len = len(code)

        encoded_binary = ''

        for i in range(0, len(code), 4):
            encoded_binary += self._encode_long(ord(code[i]) | (ord(code[i + 1]) << 8) | (ord(code[i + 2]) << 16) | (ord(code[i + 3]) << 24))
        
        return encoded_binary, code_len
 
    def _send_code(self, encoded_code, code_length, eeprom=False, run=True, progress=do_nothing):
        # Prepare and send the command we wish to run
        # 0 = Shutdown
        # 1 = Load RAM & RUN
        # 2 = Load EEPROM
        # 3 = Load EEPROM & RUN

        # I'm not comfortable with the implicit conversion of True/False to 1/0
        command = eeprom * 2 + run

        self._write_long(command)

        # If we've issued a shutdown then stop here
        if not eeprom and not run:
            return

        # Send the total length of the upload in longs
        self._write_long(code_length // 4)
        progress("Sending code ({} bytes)".format(code_length))
        
        self.serial.write(encoded_code)

        # Wait for achknowledge
        if self._read_bit(True, 8) == 1:
            raise LoaderError("RAM checksum error")
        if eeprom:
            progress("Programming EEPROM")
            if self._read_bit(True, 5) == 1:
                raise LoaderError("EEPROM programming error")
            progress("Verifying EEPROM")
            if self._read_bit(True, 2.5) == 1:
                raise LoaderError("EEPROM verification error")

    # Lowest-level functions
    def _write_byte(self, value):
        """Write a single byte of data to the serial port.
        The byte must be first transformed to represent one or more
        bits of data in the Propeller protocol.
        """
        self.serial.write(chr(value))
        
    def _write_long(self, value):
        self.serial.write(self._encode_long(value))

    def _encode_long(self, value):
        """Encode a 32-bit long as short/long pulses."""
        result = []
        for i in range(10):
            result.append(chr(0x92 | (value & 0x01) | ((value & 2) << 2) | ((value & 4) << 4)))
            value >>= 3
        result.append(chr(0xf2 | (value & 0x01) | ((value & 2) << 2)))
        return "".join(result)
        
    def _read_bit(self, echo, timeout):
        """Read a single bit back from the Propeller."""
        start = time.time()
        while time.time() - start < timeout:
            if echo:
                self._write_byte(0xf9)
                time.sleep(0.025)
            c = self.serial.read(1)
            if c:
                if c in (chr(0xfe), chr(0xff)):
                    return ord(c) & 0x01
                else:
                    raise LoaderError("Bad reply")
        raise LoaderError("Timeout error")


def upload(serial_port, path, eeprom=False, run=True, gpio_pin=-1, progress=do_nothing, terminal=False):
    """Upload file on given serial port and call the progress handler when done.

    Arguments:
    serial_port -- Serial port name in a PySerial compatible format, eg: /dev/ttyUSB0
    path -- File path to Propeller .eeprom or .binary file

    Keyword arguments:
    eeprom -- Boolean. Pass True to upload binary file at path to EEPROM otherwise
    it will be uploaded to RAM only.
    run -- Boolean. Pass True to run the uploaded binary when done.
    progress -- Progress handler, must accept a single message string.
    """
    with Loader(serial_port, gpio_pin) as loader:
        progress("Uploading {}".format(path))
        loader.upload(path=path, eeprom=eeprom, run=run, progress=progress, terminal=terminal)
        progress("Done")

    
def watch_upload(serial_port, path, delay, eeprom=False, run=True, gpio_pin=-1, progress=do_nothing):
    """Upload file on given serial port, and keep watching for changes and uploading.

    Arguments:
    serial_port -- Serial port name in a PySerial compatible format, eg: /dev/ttyUSB0
    path -- File path to Propeller .eeprom or .binary file
    delay -- Delay between file change detect and attempt to upload.

    Keyword arguments:
    eeprom -- Boolean. Pass True to upload binary file at path to EEPROM otherwise
    it will be uploaded to RAM only.
    run -- Boolean. Pass True to run the uploaded binary when done.
    progress -- Progress handler, must accept a single message string.
    """
    upload(serial_port, path, eeprom, run, gpio_pin, progress)
    progress("\nEntering watch mode. ( Ctrl+C to quit )\n")

    mtime = os.stat(path).st_mtime
    while True:
        try:
            prevMTime = mtime
            try:
                mtime = os.stat(path).st_mtime
            except OSError:
                mtime = None
            if (mtime is not None) and (mtime != prevMTime):
                progress("File change detected")
                time.sleep(delay)
                upload(serial_port, path, eeprom, run, gpio_pin, progress)
                progress("\nResuming watch mode. ( Ctrl+C to quit )\n")
            else:
                time.sleep(1)
        except LoaderError as e:
            progress(str(e) + "\n")

def detect_port(gpio_pin=-1):
    """Loop through available serial ports and detect first available Propeller."""

    for port in serial_ports():
        try:
            with Loader(port, gpio_pin) as loader:
                version = loader.get_version()
                if version > 0:
                    return (port, version)
        except (LoaderError) as e:
            continue
    return defSerial.get(os.name, "none")

def _action_get_version(args):
    """Get the version of the connected Propeller chip."""

    if args.serial == None:
        port, version = detect_port(args.gpio_pin)

        print("Found Propeller on port: " + port)
        print("Connected (version={})".format(version))

    else:
        loader = Loader(args.serial, args.gpio_pin)

        try:
            print("Connected (version={})".format(loader.get_version()))
        except LoaderError as e:
            sys.stderr.write(str(e) + "\n")
            return 1

def _action_upload(args):
    if args.filename.endswith(".eeprom"):
        args.destination = "EEPROM"
    else:
        args.destination = args.destination.upper()

    if args.serial == None:
        args.serial, version = detect_port(args.gpio_pin)
        print("Auto-detected Propeller (version={}) on port {}: ".format(version,args.serial))

    try:
        upload(args.serial, args.filename, (args.destination == "EEPROM"), args.run, args.gpio_pin, print_status, args.terminal)
    except (SystemExit, KeyboardInterrupt):
        return 3
    except Exception as e:
        sys.stderr.write(str(e) + "\n")
        return 1

def _action_watch(args):
    if args.filename.endswith(".eeprom"):
        args.destination = "EEPROM"
    else:
        args.destination = args.destination.upper()

    if args.serial == None:
        args.serial, version = detect_port(args.gpio_pin)
        print("Auto-Detected Propeller (version={}) on port {}: ".format(version,args.serial))

    try:
        watch_upload(args.serial, args.filename, args.wait, (args.destination == "EEPROM"), args.run, args.gpio_pin, print_status)
    except (SystemExit, KeyboardInterrupt) as e:
        sys.stderr.write(str(e) + "\n")
        return 1

def print_status(msg):
    """Print status messages."""
    print(msg)

if __name__ == "__main__":
    import argparse

    print("""Parallax Propeller Loader

Modified 2015 by Phil Howard
Original (C) 2007 Remy Blank
""")

    # Set up main parser
    parser = argparse.ArgumentParser()

    parser.add_argument("-v",   "--version", action="version", version="%(prog)s 0.1",
                        help="Show the program version and exit.")


    # Create parent parser for upload/watch/version common options
    p_comms = argparse.ArgumentParser(add_help=False)
    p_comms.add_argument("-s", "--serial", dest="serial", type=str, metavar="DEVICE", default=None,
                          help="Select the serial port device. The default is %(default)s.")
    p_comms.add_argument("-g", "--gpio_pin", type=int, metavar="GPIO_PIN",
                          default=-1,
                          help="Specify the GPIO pin for GPIO reset.")



    p_upload = argparse.ArgumentParser(add_help=False)
    p_upload.add_argument("filename", type=str,
                          help="Binary file to be uploaded.")
    p_upload.add_argument("-d", "--destination", type=str, default="RAM", 
                          choices=["RAM", "EEPROM"],
                          help="Upload to RAM or to EEPROM.  The default is %(default)s.")
    p_upload.add_argument("-n", "--no-run", action="store_false", dest="run", default=True,
                          help="Don't run the code after upload.")




    subparsers = parser.add_subparsers()

    parser_v = subparsers.add_parser("version", parents=[p_comms])
    parser_v.set_defaults(action=_action_get_version)

    parser_u = subparsers.add_parser("upload", parents=[p_comms, p_upload])
    parser_u.set_defaults(action=_action_upload)
    parser_u.add_argument("-t", "--terminal", action="store_true", dest="terminal", default=False,
                          help="Display output from serial after uploading.")
  
    parser_w = subparsers.add_parser("watch", parents=[p_comms, p_upload])
    parser_w.set_defaults(action=_action_watch)
    parser_w.add_argument("-wait", "--wait", type=float, metavar="DELAY",
                          default=1.0, 
                          help="Wait N seconds after detecting a file change before uploading. The default is %(default)s.")

    args = parser.parse_args()

    if hasattr(args, "action"):
        exit(args.action(args))

    parser.print_usage()
