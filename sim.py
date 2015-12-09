import time
from math import sin, cos, pi, atan, tan


def ellipsis(t, a, b, omega):
    x = a * cos(t * 2 * pi * omega)
    y = b * sin(t * 2 * pi * omega)
    theta = atan(b/(a*tan(t * 2 * pi)))
    return (x, y, theta)


def ellipsis_speed(t, a, b, omega):
    dx = - 2 * pi * omega * a * sin(t * 2 * pi * omega)
    dy = 2 * pi * omega * b * cos(t * 2 * pi * omega)
    s = dx**2 + dy**2
    return s


def get_robot_speed(robot=0):
    t = time.time()
    return ellipsis_speed(t, 1, 2, 0.1)


def get_robot_pose(robot=0):

    t = time.time()
    # let the robot follow an ellipse with semiaxis 1 and 2

    return ellipsis(t, 1, 2, 0.1)


def get_human_pose(robot=0):
    return (0, 0, 0)


def get_robot_distance(robot=0):
    return 10.0
