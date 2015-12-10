# synesthesia

## Use the leds

The leds are simulated on a webpage located at
localhost:5000/. Each led is an SVG-circle, which fill color can be set through python (via ZMQ) (and forwarded by SSE).


1. Launch the server
```bash
gunicorn -k gevent -b 0.0.0.0:5000  app:app
```

- To control the leds, import the module
```python
from sim_led import set_led
```
- and call
```python
set_led(0,(255,0,0))
```

## Use the robot

The robot is simulated in vrep. A python interface exposes pose, velocity, and (proximity) distance.

1. Launch VREP, load the scene (basic_scene.ttt), and start the simulation

- To get the robot's state, import the module
```python
from sim_vrep import get_robot_pose, get_robot_speed
from sim_vrep import get_robot_distance, get_human_pose
```

- and call
```python
x, y, theta = get_robot_pose()
speed = get_robot_speed()
distance = get_robot_distance()
x_h, y_h, theta_h = get_human_pose()
```

## Write and run a controller

The file sim_controller.py provides the skelethon for a simple controller. Complete the function
```python
def set_leds(robot_pose, robot_speed, robot_distance, human_pose):
   ...
```
that map the robot's state to the leds.

Then run
```bash
python sim_controller.py
```
