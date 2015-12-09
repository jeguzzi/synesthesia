import vrep
from math import sqrt


class VREP(object):
    """docstring for VREP"""
    def __init__(self, port):
        super(VREP, self).__init__(port)
        self.id = vrep.simxStart('127.0.0.1', port, True, True, 5000, 5)
        self.handle = {}

    def get_object_pose(self, name):
        handle = self.get_handle(name)
        _, position = vrep.simxGetObjectPosition(
            self.id, handle, -1, vrep.simx_opmode_buffer)
        _, orientation = vrep.simxGetObjectOrientation(
            self.id, handle, -1, vrep.simx_opmode_buffer)
        return (position[0], position[1], orientation[1])

    def get_object_velocity(self, name):
        handle = self.get_handle(name)
        _, lin, ang = vrep.simxGetObjectVelocity(
            self.id, handle, -1, vrep.simx_opmode_buffer)
        return lin[:2]

    def get_distance_sensor(self, name):
        handle = self.get_handle(name)
        r, s, p, h, _ = vrep.simxReadProximitySensor(
            self.id, handle, -1, vrep.simx_opmode_buffer)
        return p[2]

_vrep = VREP(9999)


def get_robot_speed(robot=0):
    lin = _vrep.get_object_velocity(robot)
    return sqrt(lin[0]**2 + lin[1]**2)


def get_robot_pose(robot=0):
    return _vrep.get_object_pose(robot)


def get_human_pose(human=0):
    return _vrep.get_object_pose(human)


def get_robot_distance(robot=0):
    return _vrep.get_distance_sensor(robot+"proximity")
