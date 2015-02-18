# Karl Palsson <karlp@tweak.net.au> 2015
"""
test methods, ie, ways of testing the serial port
"""
from __future__ import division, generators, with_statement, print_function
import logging
import random
import time
import multiprocessing

log = logging.getLogger(__name__)


class WatcherProcess(multiprocessing.Process):
    """
    Watches the port for any data received.  Compares it to what it sees on "conn" pipe

    """
    def __init__(self, port, conn):
        multiprocessing.Process.__init__(self)
        self.l = logging.getLogger(__name__)
        self.port = port
        self.conn = conn
        self.alive = multiprocessing.Event()
        self.alive.set()

    def run(self):
        expected = ""
        matching = 0
        while self.alive.is_set():
            if not self.conn.poll(0.5):
                #self.l.debug("waiting for more data....")
                continue
            newd = self.conn.recv_bytes()
            expected += newd
            self.l.debug("Still watching for: %s", expected[matching:])
            while matching < len(expected):
                rdata = self.port.read()
                #print("rx port: %s, expecting: %s" % (rdata, expected[matching]))
                if rdata == expected[matching]:
                    matching += 1
                    # TODO - can we push a status here somehow, to get a "byets outstanding" count?
                else:
                    raise ValueError("data corruption")
            print("Received %d new bytes successfully, total: %d" % (len(newd), len(expected)))
            time.sleep(0.5)
        self.l.debug("finitioissimsoo")

    def join(self, timeout=None):
        self.alive.clear()
        multiprocessing.Process.join(self, timeout)


def human(left, right=None, **kwargs):
    """
    Basic pattern test.  Aims to be somewhat like a human typing
    So very slow, normally only 1-2 bytes at a time, and only
    simple ascii.  The delay between chars is fixed to
    "human", not a function of baud rate.
    """

    wpm = kwargs.get("wpm", 90)
    bps = wpm / 1.2 # from teh ninterweb
    inter_char_target_ms = 1 / bps * 1000
    log.debug("human: target wpm: %d, interbyte ms: %f", wpm, inter_char_target_ms)
    data = b"The quick brown fox jumped over the long brown log.\n\r"
    ll = len(data)

    left.conn.send_bytes(data)

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

    data = "The jetset silver robot hammered rapidly on the machinery.\n\r"*10
    ll = len(data)
    left.conn.send_bytes(data)

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
    left.conn.send_bytes(data)

    for dat in chunker(data, a, b):
        left.write(dat)
        time.sleep(random.randrange(10,100) / 1000)
    total = time.time() - start
    print("Wrote %d bytes in %f seconds, ~bps = %f" % (ll, total, ll/total))
    print("Rough words per minute: %f" % (len(data.split()) / total *60))
