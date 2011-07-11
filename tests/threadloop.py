from __future__ import with_statement

import threading
import time
import signal

class _ThreadLoop(threading.Thread):
    """
    Convenience class for looping a function inside a background thread.
    """
    def __init__(self, func):
        """
        func can be a regular function or a generator function.

        Regular functions loop forever until they return False.

        Generator functions iterate until they yield False.
        """
        self._done = threading.Event()
        self._func = func

        threading.Thread.__init__(self)
        self.start()

    def run(self, func=None):
        if func is None:
            func = self._func

        for ret in iter(func, False):
            if self._done.isSet():
                break

            # special treatment for generator functions
            if hasattr(ret, 'next'): 
                return self.run(ret.next)

        self._done.set()

    def stop(self):
        self._done.set()
        while True:
            self.join(1)
            if not self.isAlive():
                return

    @property
    def done(self):
        return self._done.isSet()

class ThreadLoop(object):
    def __init__(self, func):
        self.thread = _ThreadLoop(func)

    def __del__(self):
        self.thread.stop()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.thread.stop()

    def __getattr__(self, attr):
        return getattr(self.thread, attr)

def test():
    def hello1():
        print "hello1"
        time.sleep(1)
        return True

    def hello2():
        while True:
            print "hello2"
            time.sleep(1)
            yield True

    def hello3():
        for i in range(3):
            print "hello3 %d" % i
            time.sleep(1)
            yield True

        print "done"

    # not Ctrl-C safe (will deadlock)
    print "NOT CTRL-C SAFE:"
    loop = ThreadLoop(hello1)
    time.sleep(3)
    loop = None

    # this is Ctrl-C safe
    print
    print "CTRL-C SAFE:"
    loop = ThreadLoop(hello1)
    try:
        time.sleep(3)
    finally:
        loop = None

    # try / finally usage example
    loop = ThreadLoop(hello2)
    try:
        for i in range(3):
            time.sleep(1)
    finally:
        loop.stop()

    # 'with' usage example
    with ThreadLoop(hello3) as loop:
        while True:
            if loop.done:
                break

            time.sleep(1)

if __name__ == "__main__":
    test()
