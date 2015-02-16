# Karl Palsson <karlp@tweak.net.au> 2015
"""
Serial port double ended testing.
"""

from __future__ import division, with_statement, generators, print_function
import argparse
import logging
import serial
import random
import time

def human(left, right=None):
    """
    Basic pattern test.  Aims to be somewhat like a human typing
    So very slow, normally only 1-2 bytes at a time, and only
    simple ascii.  The delay between chars is fixed to
    "human", not a function of baud rate.
    """
    if right:
        raise ValueError("Verification not yet supported")
    
    inter_char_target_ms = 20
    data = "The quick brown fox jumped over the long brown log.\n\r"*10
    ll = len(data)
    start = time.time()
    for x in data:
        left.write(x)
        time.sleep(random.expovariate(1/inter_char_target_ms) / 1000)
    total = time.time() - start
    print("Wrote %d bytes in %f seconds, ~bps = %f" % (ll, total, ll/total))
    print("Rough words per minute: %f" % (len(data.split()) / total *60))

def robot(left, right):
    """
    Write the text as fast as we can, but wait until it's finished
    """
    if right:
        raise ValueError("Verification not yet supported")

    data = "The jetset silver robot hammered rapidly on the machinery.\n\r"*10
    ll = len(data)
    start = time.time()
    left.write(data)
    total = time.time() - start
    print("Wrote %d bytes in %f seconds, ~bps = %f" % (ll, total, ll/total))
    print("Rough words per minute: %f" % (len(data.split()) / total *60))


def chunky_robot(left, right, a=10, b=20):
    """
    Write out the text in rapid chunks, size 'a' to 'b' bytes in length.
    Maybe pause between chunks, maybe not...
    """
    if right:
        raise ValueError("verification not yet supported")

    def chunker(source, a, b):
        """generate a-b sized chunks of source over time"""
        place = 0
        while place < len(source):
            step = random.randrange(a,b)
            yield(source[place:place+step])
            place += step
        
    data = "The chunky robot thinks in short bursts, whirring madly.\n\r"*10
    ll = len(data)
    start = time.time()
    for dat in chunker(data, a, b):
        left.write(dat)
        time.sleep(random.randrange(10,100) / 1000)
    total = time.time() - start
    print("Wrote %d bytes in %f seconds, ~bps = %f" % (ll, total, ll/total))
    print("Rough words per minute: %f" % (len(data.split()) / total *60))


def make_parser():
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-b", "--baudrate", type=int, default=19200,
        help="Baudrate to use for both ports")
    parser.add_argument("-d", "--databits", type=int, choices=[5,6,7,8],
        default=8, help="Databits for both ports")
    parser.add_argument("-p", "--parity", type=str, choices=['o','e','n','m','s'],
        default="n", help="Parity for both sides to use") 
    parser.add_argument("-s", "--stopbits", type=int, choices=[1,2],
        help="Stop bits for both ports", default=1)
    parser.add_argument("-1", "--left", type=str, required=True,
        help="device under test", metavar="DEV")
    parser.add_argument("-2", "--right", type=str, metavar="DEV",
        help="""device connected to DUT.  If provided, we will use this
        device to check what was written to the DUT, and to check 
        receive to the DUT""")
    return parser

def make_port(port, opts):
    """
    Create a serial port object based on the options given
    Eventually, this should be a proper class extending serial port?
    or a composed class probably that contains the extra stuff needed
    for collecting the output
    """
    if port:
        return serial.Serial(port,
        baudrate=opts.baudrate,
        parity=opts.parity.upper(),
        bytesize=opts.databits,
        stopbits=opts.stopbits)


def main(opts):
    """
    Open ports as required, set up a command interpreter to run the
    tests we've built.
    """

    left = make_port(opts.left, opts)
    right = make_port(opts.right, opts)

    #human(left, right)
    robot(left, right)
    chunky_robot(left, right)

if __name__ == "__main__":
    opts = make_parser().parse_args()
    main(opts)
