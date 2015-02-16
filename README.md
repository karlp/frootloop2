frootloop is for testing serial ports.

Unlike other tools I found, this one is based on the premise that you're
actually trying to test the serial port driver itself, and so it doesn't do
anything silly like expect wired loopback, which won't catch problems with
baud/parity/bytesize misconfigurations, as it simply sees it's own data back
again.

You're expected to provide two serial ports, externally connected.
If you don't provide a second port, the tool can only do a variety of writing
tests, which you will have to manually verify.  However, these can be composed
to run a sweep of a variety of settings, which may be helpful.

