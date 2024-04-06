from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor
from spike.control import wait_for_seconds, wait_until, Timer
from spike import MotorPair
from hub import port
import hub as advancedHub
import time
import math
import random

hub = PrimeHub()
timer = Timer()
contador = 1
# engine
right_engine= Motor('A')
left_engine= Motor('C')
motor_pair = MotorPair('C', 'A')
motor_pair.set_motor_rotation(3.2 * math.pi,'cm')

# color sensor
left_color = ColorSensor("F")
forward_color = ColorSensor("D")
right_color = ColorSensor("B")

#luces y sonido
proof= False
#valores
basic_blak_color=30
side_black_color=32
black_color_front=20
obstacule_distace=40
double_blck=32
recue_distance=180
global s

def update():
    global color_l
    global color_r
    color_l = left_color.get_color()
    color_r = right_color.get_color()
    global light_l
    global ligth_f
    global ligth_r
    light_l = left_color.get_reflected_light()
    ligth_f = forward_color.get_reflected_light()
    ligth_r = right_color.get_reflected_light()

def doubleblack():
    if right_color.get_reflected_light() < double_blck and left_color.get_reflected_light() < double_blck and forward_color.get_reflected_light() <20:
        motor_pair.stop()
        if proof == True:
            hub.light_matrix.write('N')
            wait_for_seconds(0.5)
            hub.light_matrix.off()
        motor_pair.move_tank(3,'degrees',left_speed=60, right_speed=60)
        if right_color.get_reflected_light() < double_blck and left_color.get_reflected_light() < double_blck and forward_color.get_reflected_light() <20:
            if proof == True :
                hub.light_matrix.write('n')
                wait_for_seconds(0.5)
                hub.light_matrix.off()
            motor_pair.move_tank(100,'degrees',left_speed=60, right_speed=60)
        else:
            motor_pair.move_tank(-16,'degrees',left_speed=60, right_speed=60)
def green():
    if right_color.get_color() =='green':
        motor_pair.stop()
        right_engine.run_for_degrees(4)
        if left_color.get_color()== 'green':
            if proof == True :
                hub.light_matrix.show_image('ARROW_N')
                wait_for_seconds(0.5)
                hub.light_matrix.off()
            turn_180_rigth()
        else:
            if proof == True :
                hub.light_matrix.show_image('ARROW_E')
                wait_for_seconds(0.5)
                hub.light_matrix.off()
            motor_pair.move_tank(180,'degrees',left_speed=60, right_speed=60)
            turn_90_right()
            motor_pair.move_tank(80,'degrees',left_speed=60, right_speed=60)
            look_left_line()
    if left_color.get_color() =='green':
        motor_pair.stop()
        left_engine.run_for_degrees(3)
        if right_color.get_color() == 'green':
            if proof == True :
                hub.light_matrix.show_image('ARROW_S')
                wait_for_seconds(0.5)
                hub.light_matrix.off()
            turn_180_rigth()
        else:
            if proof == True :
                hub.light_matrix.show_image('ARROW_W')
                wait_for_seconds(0.5)
                hub.light_matrix.off()
            motor_pair.move_tank(180,'degrees',left_speed=60, right_speed=60)
            turn_90_left()
            motor_pair.move_tank(80,'degrees',left_speed=60, right_speed=60)
            look_left_line()
def right_intersection():
    if right_color.get_reflected_light() < side_black_color and forward_color.get_reflected_light() < black_color_front:
        motor_pair.start_tank(0,0)
        if proof == True :
            hub.light_matrix.write('Td')
            wait_for_seconds(1)
            hub.light_matrix.off()
        motor_pair.move_tank(3,'degrees',left_speed=30, right_speed=30)
        if right_color.get_reflected_light() < side_black_color and forward_color.get_reflected_light() < black_color_front:
            if proof == True :
                if proof == True :
                    hub.light_matrix.show_image('YES')
                    wait_for_seconds(1)
                    hub.light_matrix.off()
            motor_pair.move_tank(100,'degrees',left_speed=60, right_speed=60)
        else:
            if proof == True :
                hub.light_matrix.write('no')
                wait_for_seconds(1)
                hub.light_matrix.off()
            motor_pair.move_tank(-15,'degrees',left_speed=60, right_speed=60)
def left_intersection():
    if left_color.get_reflected_light() < 32 and forward_color.get_reflected_light() < 32:
        motor_pair.start_tank(0,0)
        if proof == True :
            hub.light_matrix.write('Ti')
            wait_for_seconds(0.5)
            hub.light_matrix.off()
        motor_pair.move_tank(3,'degrees',left_speed=30, right_speed=30)
        if left_color.get_reflected_light() < 32 and forward_color.get_reflected_light() < 32:
            if proof == True :
                hub.light_matrix.show_image('YES')
                wait_for_seconds(1)
                hub.light_matrix.off()
            motor_pair.move_tank(100,'degrees',left_speed=60, right_speed=60)
        else:
            if proof == True :
                hub.light_matrix.write('no')
                wait_for_seconds(1)
                hub.light_matrix.off()
            motor_pair.move_tank(-15,'degrees',left_speed=60, right_speed=60)
def look_rigth_line():
    motor_pair.stop()
    wait_for_seconds(1)
    hub.motion_sensor.reset_yaw_angle()
    if proof == True :
        hub.light_matrix.write('Cde')
    motor_pair.start_tank(-30,30)
    while (hub.motion_sensor.get_yaw_angle() < -10):
        print(hub.motion_sensor.get_yaw_angle())
    motor_pair.stop()
    motor_pair.start_tank(30,-30)
    while(right_color.get_reflected_light() > 30):
        print('sensor derecho')
    motor_pair.stop()
    angle = hub.motion_sensor.get_yaw_angle()

def look_left_line():
    motor_pair.stop()
    wait_for_seconds(1)
    hub.motion_sensor.reset_yaw_angle()
    if proof == True :
        hub.light_matrix.write('Ciz')
    motor_pair.start_tank(30,-30)
    while (hub.motion_sensor.get_yaw_angle() < -10):
        print(hub.motion_sensor.get_yaw_angle())
    motor_pair.stop()
    motor_pair.start_tank(-30,30)
    while(left_color.get_reflected_light() > 30):
        print('sensor izquierdo')
    motor_pair.stop()
    angle = hub.motion_sensor.get_yaw_angle()

def turn_90_left():
    motor_pair.start_tank(0,0)
    wait_for_seconds(1)
    hub.motion_sensor.reset_yaw_angle()
    motor_pair.start_tank(30,-30)
    while (hub.motion_sensor.get_yaw_angle() >-85):
        print(hub.motion_sensor.get_yaw_angle())
    motor_pair.start_tank(0,0)
    if proof == True :
        hub.speaker.beep(60, 1)
    #wait_for_seconds(1)
    angle = hub.motion_sensor.get_yaw_angle()
    # print('Angulo:', angle)

def turn_90_right():
    motor_pair.start_tank(0,0)
    wait_for_seconds(1)
    hub.motion_sensor.reset_yaw_angle()
    motor_pair.start_tank(-30,30)
    while (hub.motion_sensor.get_yaw_angle() < 85):
        print(hub.motion_sensor.get_yaw_angle())
    motor_pair.start_tank(0,0)
    if proof == True :
        hub.speaker.beep(60, 1)
    # wait_for_seconds(1)
    angle = hub.motion_sensor.get_yaw_angle()
    # print('Angulo:', angle)

def turn_180_rigth():
    turn_90_left()
    turn_90_left()
    motor_pair.move_tank(0.7,'cm',30,-30)

def turn_180_left():
    turn_90_right()
    turn_90_right()
    motor_pair.move_tank(0.7,'cm',-30,30)

def turn_90_rigth_rescue():
    motor_pair.start_tank(0,0)
    wait_for_seconds(1)
    hub.motion_sensor.reset_yaw_angle()
    motor_pair.start_tank(-20,40)
    while (hub.motion_sensor.get_yaw_angle() < 83):
        print(hub.motion_sensor.get_yaw_angle())
    motor_pair.start_tank(0,0)
    if proof == True :
        hub.speaker.beep(60, 1)
    # wait_for_seconds(1)
    angle = hub.motion_sensor.get_yaw_angle()
    # print('Angulo:', angle)

def turn_90_left_rescue():
    motor_pair.start_tank(0,0)
    wait_for_seconds(1)
    hub.motion_sensor.reset_yaw_angle()
    motor_pair.start_tank(40,-20)
    while (hub.motion_sensor.get_yaw_angle() >-83):
        print(hub.motion_sensor.get_yaw_angle())
    motor_pair.start_tank(0,0)
    if proof == True :
        hub.speaker.beep(60, 1)
    #wait_for_seconds(1)
    angle = hub.motion_sensor.get_yaw_angle()
    # print('Angulo:', angle)



# def rescate_izquierda():
#     global esquina
#     rescate_v1=0
#     leedistancia()
#     verificalectura()
#     #print(derarriba)
#     while rescate_v1 <3:
#         motor_pair.start_tank(100,98)
#         leedistancia()
#         print(leedistancia,)
#         verificalectura()
#         #print(derarriba)
#         while derarriba > recue_distance:
#             leedistancia()
#             print( derarriba , 'izquierda')
#         if forward_color.get_reflected_light() < 20:
#             motor_pair.stop()
#             esquina=rescate_v1+2
#             motor_pair.move_tank(110, 'degrees', left_speed=-80, right_speed=-80)
#             wait_for_seconds(1)
#             mueveservoarriba()
#             wait_for_seconds(1)
#             motor_pair.move_tank(600, 'degrees', left_speed=-80, right_speed=-80)
#             motor_pair.stop()
#             mueveservoabajo()
#             wait_for_seconds(1)
#         motor_pair.stop()
#         if proof == True :
#             hub.light_matrix.write('Rd')
#             wait_for_seconds(1)
#             hub.light_matrix.off()
#         motor_pair.stop()
#         turn_90_rigth_rescue()
#         motor_pair.move_tank(800, 'degrees', left_speed=-90, right_speed=-90)
#         leedistancia()
#         verificalectura()
#         #print(derarriba)
#         rescate_v1= rescate_v1 + 1
#     esquinas_iz()

# def rescate_derecha():
#     global esquina
#     rescate_v1=0
#     while rescate_v1 <3:
#         motor_pair.start_tank(98,100)
#         leedistancia()
#         verificalectura()
#         #print(derarriba)
#         while derarriba > recue_distance:
#             leedistancia()
#             verificalectura()
#             print( derarriba , 'derecha')
#         if forward_color.get_reflected_light() < 20:
#             esquina= rescate_v1 +2
#             motor_pair.stop()
#             motor_pair.move_tank(110, 'degrees', left_speed=-80, right_speed=-80)
#             wait_for_seconds(1)
#             mueveservoarriba()
#             wait_for_seconds(1)
#             motor_pair.move_tank(600, 'degrees', left_speed=-80, right_speed=-80)
#             motor_pair.stop()
#             mueveservoabajo()
#             wait_for_seconds(1)
#         motor_pair.stop()
#         if proof == True :
#             hub.light_matrix.write('Rd')
#             wait_for_seconds(1)
#             hub.light_matrix.off()
#         motor_pair.stop()
#         turn_90_left_rescue()
#         motor_pair.move_tank(800, 'degrees', left_speed=-90, right_speed=-90)
#         leedistancia()
#         verificalectura()
#         #print(derarriba)
#         rescate_v1= rescate_v1 + 1
#     esquina_der()

# def rescate_inicio():
#     global esquina
#     motor_pair.stop()
#     leedistancia()
#     verificalectura()
#     #print(derarriba)
#     if derarriba < 280:
#         motor_pair.stop()
#         if proof == True :
#             hub.light_matrix.write('180')
#             wait_for_seconds(1)
#             hub.light_matrix.off()
#         #motor_pair.move_tank(10, 'cm', left_speed=-75, right_speed=-75)
#         turn_180_left()
#         motor_pair.move_tank(800, 'degrees', left_speed=-90, right_speed=-90)
#         motor_pair.stop()
#         leedistancia()
#         verificalectura()
#         #print(derarriba)
#         rescate_izquierda()
#         esquinas_iz()
#     else:
#         motor_pair.stop()
#         if proof == True :
#             hub.light_matrix.write('-')
#             wait_for_seconds(1)
#             hub.light_matrix.off()
#         motor_pair.stop()
#         wait_for_seconds(0.5)
#         motor_pair.move_tank(800, 'degrees', left_speed=-90, right_speed=-90)
#         leedistancia()
#         verificalectura()
#         #print(derarriba)
#         rescate_derecha()
#         esquina_der()
#     angle = hub.motion_sensor.get_yaw_angle()


# esquina=1
# def esquina_der():
#     global esquina_derecha
#     if esquina == 1:
#         motor_pair.start_tank(100,98)
#         leedistancia()
#         verificalectura()
#         #print(derarriba)
#         while derarriba > recue_distance:
#             leedistancia()
#             verificalectura()
#             print( derarriba , 'derecha')
#         if forward_color.get_reflected_light() < 20:
#             motor_pair.stop()
#             motor_pair.move_tank(110, 'degrees', left_speed=-80, right_speed=-80)
#             wait_for_seconds(1)
#             mueveservoarriba()
#             wait_for_seconds(1)
#             motor_pair.move_tank(600, 'degrees', left_speed=-80, right_speed=-80)
#             motor_pair.stop()
#             mueveservoabajo()
#             wait_for_seconds(1)
#         motor_pair.stop()
#     elif esquina == 2:
#         motor_pair.move_tank(650, 'degrees', left_speed=60, right_speed=60)
#         motor_pair.stop()
#         hub.motion_sensor.reset_yaw_angle()
#         motor_pair.start_tank(50,-50)
#         while (hub.motion_sensor.get_yaw_angle() > -60):
#             a=1
#         motor_pair.stop()
#         motor_pair.start_tank(100,98)
#         leedistancia()
#         verificalectura()
#         #print(derarriba)
#         while derarriba > recue_distance:
#             leedistancia()
#             verificalectura()
#             print( derarriba , 'derecha')
#         if forward_color.get_reflected_light() < 20:
#             motor_pair.stop()
#             motor_pair.move_tank(110, 'degrees', left_speed=-80, right_speed=-80)
#             wait_for_seconds(1)
#             mueveservoarriba()
#             wait_for_seconds(1)
#             motor_pair.move_tank(600, 'degrees', left_speed=-80, right_speed=-80)
#             motor_pair.stop()
#             mueveservoabajo()
#             wait_for_seconds(1)
#         motor_pair.stop()
#     elif esquina == 3:
#         motor_pair.move_tank(2000, 'degrees', left_speed=80, right_speed=80)
#         motor_pair.stop()
#         hub.motion_sensor.reset_yaw_angle()
#         motor_pair.start_tank(50,-50)
#         while (hub.motion_sensor.get_yaw_angle() > -120):
#             a=1
#         motor_pair.stop()
#         motor_pair.start_tank(98,100)
#         leedistancia()
#         verificalectura()
#         #print(derarriba)
#         while derarriba > recue_distance:
#             leedistancia()
#             verificalectura()
#             print( derarriba , 'derecha')
#         if forward_color.get_reflected_light() < 20:
#             motor_pair.stop()
#             motor_pair.move_tank(110, 'degrees', left_speed=-80, right_speed=-80)
#             wait_for_seconds(1)
#             mueveservoarriba()
#             wait_for_seconds(1)
#             motor_pair.move_tank(600, 'degrees', left_speed=-80, right_speed=-80)
#             motor_pair.stop()
#             mueveservoabajo()
#             wait_for_seconds(1)
#         motor_pair.stop()

# def esquinas_iz():
#     global esquina
#     if esquina== 1:
#         motor_pair.start_tank(98,100)
#         leedistancia()
#         verificalectura()
#         #print(derarriba)
#         while derarriba > recue_distance:
#             leedistancia()
#             verificalectura()
#             print( derarriba , 'derecha')
#         if forward_color.get_reflected_light() < 20:
#             motor_pair.stop()
#             motor_pair.move_tank(110, 'degrees', left_speed=-80, right_speed=-80)
#             wait_for_seconds(1)
#             mueveservoarriba()
#             wait_for_seconds(1)
#             motor_pair.move_tank(600, 'degrees', left_speed=-80, right_speed=-80)
#             motor_pair.stop()
#             mueveservoabajo()
#             wait_for_seconds(1)
#         motor_pair.stop()
#     elif esquina == 2:
#         motor_pair.move_tank(650, 'degrees', left_speed=90, right_speed=90)
#         motor_pair.stop()
#         hub.motion_sensor.reset_yaw_angle()
#         motor_pair.start_tank(-50,50)
#         while (hub.motion_sensor.get_yaw_angle() < 60):
#             a=1
#         motor_pair.stop()
#         motor_pair.start_tank(100,100)
#         leedistancia()
#         verificalectura()
#         #print(derarriba)
#         while derarriba > recue_distance:
#             leedistancia()
#             verificalectura()
#             print( derarriba , 'derecha')
#         if forward_color.get_reflected_light() < 20:
#             motor_pair.stop()
#             motor_pair.move_tank(110, 'degrees', left_speed=-90, right_speed=-90)
#             wait_for_seconds(1)
#             mueveservoarriba()
#             wait_for_seconds(1)
#             motor_pair.move_tank(600, 'degrees', left_speed=-90, right_speed=-90)
#             motor_pair.stop()
#             mueveservoabajo()
#             wait_for_seconds(1)
#         motor_pair.stop()
#         motor_pair.move_tank(200, 'degrees', left_speed=-90, right_speed=-90)
#     elif esquina == 3:
#         motor_pair.move_tank(2000, 'degrees', left_speed=100, right_speed=100)
#         motor_pair.stop()
#         hub.motion_sensor.reset_yaw_angle()
#         motor_pair.start_tank(-50,50)
#         while (hub.motion_sensor.get_yaw_angle() < 120):
#             a=1
#         motor_pair.stop()
#         motor_pair.start_tank(98,100)
#         leedistancia()
#         verificalectura()
#         #print(derarriba)
#         while derarriba > recue_distance:
#             leedistancia()
#             verificalectura()
#             print( derarriba , 'derecha')
#         if forward_color.get_reflected_light() < 20:
#             motor_pair.stop()
#             motor_pair.move_tank(110, 'degrees', left_speed=-90, right_speed=-90)
#             wait_for_seconds(1)
#             mueveservoarriba()
#             wait_for_seconds(1)
#             motor_pair.move_tank(600, 'degrees', left_speed=-90, right_speed=-90)
#             motor_pair.stop()
#             mueveservoabajo()
#             wait_for_seconds(1)
#         motor_pair.stop()

# def rescate():
    global esquina_derecha
    global esquina_izquierda
    if forward_color.get_green() > 950 and forward_color.get_blue() > 950 and forward_color.get_red() > 950 :            #izarriba derarriba izabajo derabajo
        motor_pair.stop()
        wait_for_seconds(1)
        mueveservoabajo()
        wait_for_seconds(2)
        motor_pair.start_tank(100,98)
        leedistancia()
        verificalectura()
        while (derarriba > recue_distance):
            leedistancia()
            verificalectura()
            #print(derarriba)
        motor_pair.stop()
        if forward_color.get_reflected_light() < 20:
            motor_pair.stop()
            wait_for_seconds(2)
            motor_pair.move_tank(110, 'degrees', left_speed=-90, right_speed=-90)
            mueveservoarriba()
            wait_for_seconds(1)
            motor_pair.move_tank(600, 'degrees', left_speed=-90, right_speed=-90)
            motor_pair.stop()
            mueveservoabajo()
            wait_for_seconds(2)
            esquina=1
        motor_pair.stop()
        hub.motion_sensor.reset_yaw_angle()
        motor_pair.start_tank(40,-40)
        while (hub.motion_sensor.get_yaw_angle() > -89):
            a=1
        motor_pair.stop()
        while True:
            rescate_inicio()
    angle = hub.motion_sensor.get_yaw_angle()

#########################################################################################################################################################################################
#################################################################################### MAIN CODE ##########################################################################################
#########################################################################################################################################################################################

controlPID = False
tanterior = 0.01
tiempo = 0.01
integral = 0.0
derivada = 0.0
error_previo = 0.0
cuenta = -1


while True:
    #global cuenta
    global color_l
    global color_r
    global light_l
    global ligth_f
    global ligth_r
    cuenta = cuenta + 1
    color_l = left_color.get_color()
    color_r = right_color.get_color()
    light_l = left_color.get_reflected_light()
    ligth_f = forward_color.get_reflected_light()
    ligth_r = right_color.get_reflected_light()    
    #if cuenta%20 == 0:
     #   pidedistancia()

    if controlPID == True:
        velocidad = 18
        kp = 1.2    # 3.95 antes
        ki = 0.0    # 0.02 antes
        kd = 0.15   # 0.4antes
        tanterior = tiempo
        tiempo = time.ticks_ms()
        dt = tiempo - tanterior
        error = ligth_r - light_l
        proporcional = error
        integral = integral+ error * 0.005
        derivada = (error - error_previo)
        #    salida = int(kp * proporcional + ki * integral + kd * derivada)
        error_previo = error
        salida = int(kp * proporcional + ki * integral + kd * derivada)
        #print(error, derivada, integral, salida, velocidad + salida, velocidad - salida, dt)
        motor_pair.start_tank(velocidad + salida,velocidad - salida)
    else:
        if left_color.get_reflected_light() > basic_blak_color:
            right_engine.start_at_power(38)
        else:
            right_engine.start_at_power(-55)
        if right_color.get_reflected_light() > basic_blak_color:
            left_engine.start_at_power(-38)
        else:
            left_engine.start_at_power(55)

    if light_l < 30 or ligth_r < 30 or ligth_f < 40 :
        timer.reset()
    
    if timer.now() > 2.5:
        motor_pair.stop()
        motor_pair.start_tank(-30,-30)
        while (left_color.get_reflected_light() > 30 and right_color.get_reflected_light() > 30 and forward_color.get_reflected_light() > 40):
            print('sin linea')
        motor_pair.stop()
        if left_color.get_reflected_light() < 30:
            right_engine.run_for_degrees(100,-45)
            motor_pair.stop()
        else:
            if right_color.get_reflected_light() < 30:
                left_engine.run_for_degrees(100, 45)# bien
                motor_pair.stop()

    green()
    doubleblack()
    right_intersection()
    left_intersection()
    #rescate()
