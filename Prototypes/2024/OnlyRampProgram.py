from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor
from spike.control import wait_for_seconds, wait_until, Timer
from spike import MotorPair
import hub
import math

right_engine= Motor('A')
left_engine= Motor('C')
motor_pair = MotorPair('C', 'A')
motor_pair.set_motor_rotation(3.2 * math.pi,'cm')

# color sensor
left_color = ColorSensor("F")
forward_color = ColorSensor("D")
right_color = ColorSensor("B")

basic_blak_color=30


while True:
    if left_color.get_reflected_light() > basic_blak_color:#follows the line asked if it detects black it goes backwards but forwards
        right_engine.start_at_power(40)
    else:
        right_engine.start_at_power(-60)
    if right_color.get_reflected_light() > basic_blak_color:
        left_engine.start_at_power(-40)
    else:
        left_engine.start_at_power(60)
