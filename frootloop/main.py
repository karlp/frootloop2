# Karl Palsson <karlp@tweak.net.au> 2015
"""
Serial port double ended testing.
"""

from __future__ import division, with_statement, generators, print_function
import argparse
import logging
import multiprocessing
import serial

import frootloop
import frootloop.cli

logging.basicConfig(level=logging.DEBUG)



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
        logging.debug("Creating port for %s", port)
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
    if right:
        left.conn, right.conn = multiprocessing.Pipe()

    cmdloop = frootloop.cli.Frootloop(left, right, opts)
    cmdloop.cmdloop()

if __name__ == "__main__":
    opts = make_parser().parse_args()
    main(opts)
