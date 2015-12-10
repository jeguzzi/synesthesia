import zmq.green as zmq

port = 5556

context = zmq.Context()
sock = context.socket(zmq.PUSH)
sock.connect("tcp://localhost:%d" % port)


def set_led(led, rgb):
    """Set the led with id <led> to an rgb (r,g,b)"""
    sock.send_json((led, rgb))
