import random
import gevent
from sim_led import set_led
from sim_vrep import get_human_pose
from sim_vrep import get_robot_pose, get_robot_speed, get_robot_distance
from sim_vrep import cleanup
from math import sin, pi

# import the same functions but from different modules to carry the program to
# the real world (led strip, real robots)


def set_wave_leds(t):
    """An wave travelling along the strip"""
    for i in range(0, 10):
        r = int(255*sin((i/10.0-t/10.0)*2*pi)**2)
        g = int(255*sin((i/10.0+t/10.0)*2*pi)**2)
        b = int(255*sin((i/15.0-t/5.0)*2*pi)**2)
        set_led(i, (r, g, b))


def set_random_leds():
    """A random walk of the leds"""
    for i in range(0, 10):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        set_led(i, (r, g, b))


def set_leds(robot_pose, robot_speed, robot_distance, human_pose):
    """Map robot's state to leds"""
    # This is the entry point for Isabella's code.
    # Extend this function to implement the interface.

    # Here is just one example

    x, y, theta = robot_pose
    set_led(0, [int(x*100), 0, 0])
    set_led(1, [0, int(y*100), 0])
    set_led(2, [0, 0, int(theta*100)])
    set_led(3, [0, 0, int(robot_distance*100)])


def update(t):
    """Do a control step"""
    # Get the robot state
    robot_pose = get_robot_pose()
    robot_speed = get_robot_speed()
    robot_distance = get_robot_distance()
    human_pose = get_human_pose()
    # Update the leds
    set_leds(robot_pose, robot_speed, robot_distance, human_pose)


def start():
    """Start the control loop"""
    g = gevent.spawn(run)
    gevent.joinall([g])


def run():
    """The main control loop"""
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
