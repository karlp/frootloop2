# Karl Palsson <karlp@tweak.net.au> 2015
"""
Run a command interpreter cli for easier manual testing
"""

import cmd
import logging
import frootloop.froot



class Frootloop(cmd.Cmd):
    """
    cmd loop interactive mode for frootloop diagnostic tools
    """
    def __init__(self, left, right, opts):
        cmd.Cmd.__init__(self)
        self.left = left
        self.right = right
        self.opts = opts
        self.l = logging.getLogger(__name__)

    def do_human(self, args):
        """
        human [wpm]
        Simulate a human typing onto the serial port
        :param wpm: desired Words Per Minute (roughly)
        :return:
        """
        if args:
            aa = args.split()
            try:
                wpm = int(aa[0], base=0)
            except ValueError:
                print("argument must be numeric!")
                return
            frootloop.froot.human(self.left, self.right, wpm=wpm)
        else:
            frootloop.froot.human(self.left, self.right)

    def do_robot(self, args):
        """
        Simulate a blaster, writing entire data blocks as fast as allowed
        TODO - provide a way to make sure it crosses buffer sizes!
        :param args:
        :return:
        """
        frootloop.froot.robot(self.left, self.right)

    def do_chunky(self, args):
        """

        :param args:
        :return:
        """
        frootloop.froot.chunky_robot(self.left, self.right)

    def do_baud(self, args):
        """
        with no arguments, show the baudrate of both ports
        with one argument, apply that baudrate to both ports
        with two arguments, apply those to each.
        :param args:
        :return:
        """

        if args:
            bauds = map(int, args.split())
            self.left.setBaudrate(bauds[0])
            if len(bauds) > 1:
                self.right.setBaudrate(bauds[1])
            else:
                self.right.setBaudrate(bauds[0])

        else:
            print("Current baud is left: %d, right: %d" % (self.left.getBaudrate(), self.right.getBaudrate()))

    def do_EOF(self, args):
        return self.do_exit(args)

    def do_exit(self, args):
        return True

    def cmdloop(self):
        while True:
            try:
                cmd.Cmd.cmdloop(self)
            except KeyboardInterrupt:
                print(" - interrupted")
                continue
            break
