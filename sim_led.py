import zmq.green as zmq

port = 5556

context = zmq.Context()
sock = context.socket(zmq.PUSH)
sock.connect("tcp://localhost:%d" % port)


def set_led(led, rgb):
    sock.send_json((led, rgb))
