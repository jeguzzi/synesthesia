import random
import gevent
from sim_led import set_led
from sim_vrep import get_human_pose
from sim_vrep import get_robot_pose, get_robot_speed, get_robot_distance
from sim_vrep import cleanup
from math import sin, pi


def set_wave_leds(t):
    for i in range(0, 10):
        r = int(255*sin((i/10.0-t/10.0)*2*pi)**2)
        g = int(255*sin((i/10.0+t/10.0)*2*pi)**2)
        b = int(255*sin((i/15.0-t/5.0)*2*pi)**2)
        set_led(i, (r, g, b))


def set_random_leds():
    for i in range(0, 10):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        set_led(i, (r, g, b))


def set_leds(robot_pose, robot_speed, robot_distance, human_pose):
    x, y, theta = robot_pose
    # prendo tutti i dati e li trasformo in led
    
    set_led(0, [int(x*100), 0, 0])
    set_led(1, [0, int(y*100), 0])
    set_led(2, [0, 0, int(theta*100)])
    set_led(3, [0, 0, int(robot_distance*100)])


def update(t):
    # print 'Do one update step'
    robot_pose = get_robot_pose()
    robot_speed = get_robot_speed()
    robot_distance = get_robot_distance()
    human_pose = get_human_pose()
    # print 'Newest pose and distance', pose, distance
    # set_random_leds()
    # set_wave_leds(t)

    set_leds(robot_pose, robot_speed, robot_distance, human_pose)


def start():
    g = gevent.spawn(run)
    gevent.joinall([g])


def run():
    t = 0
    dt = 0.05
    while True:
        update(t)
        gevent.sleep(dt)
        t += dt


if __name__ == '__main__':
    try:
        start()
    except:
        pass
    finally:
        cleanup()
