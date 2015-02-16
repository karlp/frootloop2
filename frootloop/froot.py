# Karl Palsson <karlp@tweak.net.au> 2015
"""
test methods, ie, ways of testing the serial port
"""
from __future__ import division, generators, with_statement, print_function
import logging
import random
import time

log = logging.getLogger(__name__)

def human(left, right=None, **kwargs):
    """
    Basic pattern test.  Aims to be somewhat like a human typing
    So very slow, normally only 1-2 bytes at a time, and only
    simple ascii.  The delay between chars is fixed to
    "human", not a function of baud rate.
    """
    if right:
        raise ValueError("Verification not yet supported")

    wpm = kwargs.get("wpm", 90)
    bps = wpm / 1.2 # from teh ninterweb
    inter_char_target_ms = 1 / bps * 1000
    log.debug("human: target wpm: %d, interbyte ms: %f", wpm, inter_char_target_ms)
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
