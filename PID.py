from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *
import math
hub = PrimeHub()
right_engine= Motor('A')
left_engine= Motor('C')
motor_pair = MotorPair('C', 'A')
motor_pair.set_motor_rotation(3.2 * math.pi,'cm')

# color sensor
left_color = ColorSensor("F")
forward_color = ColorSensor("D")
right_color = ColorSensor("B")

luz_1 = left_color.get_reflected_light()
luz_2 = forward_color.get_reflected_light()
luz_3 = right_color.get_reflected_light()
base=20
kp= 1

while True:
    diferencia=left_color.get_reflected_light() - right_color.get_reflected_light()
    potencia_izquierda= int(base+ diferencia * kp)
    potencia_derecha=int(base- diferencia * kp)
    print(diferencia)
    print(potencia_derecha , potencia_izquierda)
    motor_pair.start_tank(potencia_derecha,potencia_izquierda)
    #    wait_for_seconds(0.1)
