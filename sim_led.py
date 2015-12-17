import zmq.green as zmq
import threading
import time
from math import sin, exp, pi

port = 5556

context = zmq.Context()
sock = context.socket(zmq.PUSH)
sock.connect("tcp://localhost:%d" % port)


def set_led(led, rgb):
    """Set the led with id <led> to an rgb (r,g,b)"""
    sock.send_json((led, [rgb]))


def set_led_list(led, rgbs):
    """Set the led starting with id <led> to an rgb list [(r,g,b)]"""
    sock.send_json((led, rgbs))


def _wave(center, color, t, period=-1, width=0):
    if period > 0:
        a = sin(pi * t / period) ** 2
    else:
        a = 1
    if width > 0:
        def f(led):
            b = a * exp(-(float(led - center) / width) ** 2)
            return tuple([int(b * c) for c in color])
    else:
        def f(led):
            if led == center:
                return tuple([int(a * c) for c in color])
            else:
                return (0, 0, 0)
    return f


class Wave(threading.Thread):
    """docstring for Wave"""
    def __init__(self):
        super(Wave, self).__init__()
        self.width = 0
        self.period = -1
        self.color = (255, 255, 255)
        self.center = 0
        self.run_loop_period = 0.04
        self.n = 20
        self._on = True
        self._stop = False

    def pause(self):
        self._on = False

    def restart(self):
        self._on = True

    def exit(self):
        self._stop = True

    def run(self):
        while not self._stop:
            if self._on:
                t = time.time()
                f = _wave(self.center, self.color, t, self.period, self.width)
                colors = [f(led) for led in range(0, self.n)]
                set_led_list(0, colors)
            time.sleep(self.run_loop_period)
