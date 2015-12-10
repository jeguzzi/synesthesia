import vrep
from math import sqrt
import time


class VREP(object):
    """docstring for VREP"""

    def __init__(self, port):
        super(VREP, self).__init__()
        # Add simExtRemoteApiStart(<port>) to the init script of VREP
        self.id = vrep.simxStart('127.0.0.1', port, True, False, 5000, 5)
        self._handle = {}
        self._p = []
        self._v = []
        self._s = []

    def __del__(self):
        vrep.simxFinish(self.id)

    def get_handle(self, name):
        if name in self._handle:
            return self._handle[name]

        r, handle = vrep.simxGetObjectHandle(self.id, name,
                                             vrep.simx_opmode_oneshot_wait)
        if r == vrep.simx_return_ok:
            self._handle[name] = handle
            return handle
        else:
            raise NameError('Handle not found %s' % r)

    def get_object_pose(self, name):
        handle = self.get_handle(name)

        if handle not in self._p:
            vrep.simxGetObjectPosition(
                self.id, handle, -1, vrep.simx_opmode_streaming)
            vrep.simxGetObjectOrientation(
                self.id, handle, -1, vrep.simx_opmode_streaming)
            self._p.append(handle)
            time.sleep(0.5)

        r, position = vrep.simxGetObjectPosition(
            self.id, handle, -1, vrep.simx_opmode_buffer)
        if r != vrep.simx_return_ok:
            raise NameError('Position unknown')
        r, orientation = vrep.simxGetObjectOrientation(
            self.id, handle, -1, vrep.simx_opmode_buffer)
        if r != vrep.simx_return_ok:
            raise NameError('Orientation unknown')
        return (position[0], position[1], orientation[2])

    def get_object_velocity(self, name):
        handle = self.get_handle(name)
        if handle not in self._v:
            vrep.simxGetObjectVelocity(
                self.id, handle, vrep.simx_opmode_streaming)
            self._v.append(handle)
            time.sleep(0.5)

        r, lin, ang = vrep.simxGetObjectVelocity(
            self.id, handle, vrep.simx_opmode_buffer)

        if r != vrep.simx_return_ok:
            raise NameError('Velocity unknown')
        return lin[:2]

    def get_distance_sensor(self, name):
        handle = self.get_handle(name)
        if handle not in self._s:
            vrep.simxReadProximitySensor(
                self.id, handle, vrep.simx_opmode_streaming)
            self._s.append(handle)
            time.sleep(0.5)

        r, s, p, h, _ = vrep.simxReadProximitySensor(
            self.id, handle, vrep.simx_opmode_buffer)
        if r != vrep.simx_return_ok:
            raise NameError('Sensor unknown')
        return p[2]

_vrep = VREP(9999)
_default_human = 'Bill'
_default_robot = 'bubbleRob'


def cleanup():
    global _vrep
    del _vrep


def get_robot_speed(robot=None):
    if robot is None:
        robot = _default_robot
    lin = _vrep.get_object_velocity(robot)
    return sqrt(lin[0]**2 + lin[1]**2)


def get_robot_pose(robot=None):
    if robot is None:
        robot = _default_robot
    return _vrep.get_object_pose(robot)


def get_human_pose(human=None):
    if human is None:
        human = _default_human
    return _vrep.get_object_pose(human)


def get_robot_distance(robot=None, prox='sensingNose'):
    if robot is None:
        robot = _default_robot
    return _vrep.get_distance_sensor(prox)
