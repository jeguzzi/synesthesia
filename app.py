from flask import Flask, render_template, Response
from sse import MyServerSentEvent as SSE
from gevent.queue import Queue
import zmq.green as zmq
import gevent
import logging
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('main.html')


@app.route('/see')
def sse():
    return Response(stream_led(), mimetype="text/event-stream")


subscriptions = []


def stream_led():
    q = Queue()
    subscriptions.append(q)
    try:
        while True:
            try:
                (led, color) = q.get()
            except Exception, e:
                logging.error(e)
                break
            # Send a list of colors
            svg_color = ['rgb({r},{g},{b})'.format(r=r, g=g, b=b)
                         for (r, g, b) in color]
            # Send a single color
            # (r, g, b) = color
            # svg_color = 'rgb({r},{g},{b})'.format(r=r, g=g, b=b)
            ev = SSE(svg_color)
            ev.id = led + 1
            yield ev.encode()
    except GeneratorExit:  # Or maybe use flask signals
        app.logger.debug("Stream terminated")
    finally:
        subscriptions.remove(q)


def set_led(led, rgb):
    for q in subscriptions:
        q.put((led, rgb))


def init_app():
    gevent.spawn(listen)


port = 5556


def listen():
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:%d" % port)
    # print 'listening...'
    while True:
        led, color = socket.recv_json()
        set_led(led, color)

init_app()

if __name__ == '__main__':
    app.run(debug=True)
