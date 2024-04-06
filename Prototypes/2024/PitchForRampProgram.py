from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, 
from spike.control import wait_for_seconds, wait_until, Timer
from spike import MotorPair
import hub
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

basic_blak_color=30
down_blak_color=50    

def LineTrackingA():
    global basic_blak_color, down_blak_color

    print("Line Tracking A Starting")


    while True:
        pitch = hub.motion_sensor.get_pitch_angle()

        if 3 <= pitch <= 25:
            print("Arriba")
            if left_color.get_reflected_light() > basic_blak_color:
                right_engine.start_at_power(50)
            else:
                right_engine.start_at_power(-70)
            if right_color.get_reflected_light() > basic_blak_color:
                left_engine.start_at_power(-50)
            else:
                left_engine.start_at_power(70)
        elif 0 <= pitch <= 1 or pitch == -1:
            print("Normal")
            if left_color.get_reflected_light() > basic_blak_color:
                right_engine.start_at_power(30)
            else:
                right_engine.start_at_power(-50)
            if right_color.get_reflected_light() > basic_blak_color:
                left_engine.start_at_power(-30)
            else:
                left_engine.start_at_power(50)
        elif -5 >= pitch <= -20:
            print("Abajo")
            if left_color.get_reflected_light() > basic_blak_color:
                right_engine.start_at_power(25)
            else:
                right_engine.start_at_power(-35)
            if right_color.get_reflected_light() > basic_blak_color:
                left_engine.start_at_power(-25)
            else:
                left_engine.start_at_power(35)




LineTrackingA()
