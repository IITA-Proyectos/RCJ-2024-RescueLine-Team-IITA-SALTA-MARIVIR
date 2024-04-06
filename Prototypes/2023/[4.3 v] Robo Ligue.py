from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor
from spike.control import wait_for_seconds, wait_until, Timer
from spike import MotorPair
from hub import port
import hub as advancedHub
import time
import math
import random

port.E.mode(port.MODE_FULL_DUPLEX)
a=port.E
wait_for_seconds(1)
a.baud(115200)
firmapaquete = "0000"
izarriba = 0
derarriba = 0
izabajo = 0
derabajo = 0


def nextmsg():
    global firmapaquete
    firmapaquete = int(firmapaquete)
    if firmapaquete == 9999:
        firmapaquete = "0000"
        return
    firmapaquete = str(firmapaquete + 1)
    while len(firmapaquete)<4:
        firmapaquete = "0"+firmapaquete

def mueveservoarriba():
    global izarriba
    global derarriba
    global izabajo
    global derabajo
    global firmapaqquete
    nextmsg()
    mensaje = 'A' + firmapaquete + "-"
    try:
        a.write(mensaje)
        s=a.read(100).decode()
        cod = s[0:5]
        #print(s)
        #print(s[6:10])
        #print(s[11:15])
        #print(s[16:20])
        #print(s[21:25])
        izarriba = int(s[6:10])
        derarriba = int(s[11:15])
        izabajo = int(s[16:20])
        derabajo = int(s[21:25])
        return
    except:
        izarriba =9999
        derarriba = 9999
        izabajo =9999
        derabajo =9999
        return

def mueveservoabajo():
    global izarriba
    global derarriba
    global izabajo
    global derabajo
    global firmapaqquete
    nextmsg()
    mensaje = 'B' + firmapaquete + "-"
    try:
        a.write(mensaje)
        s=a.read(100).decode()
        cod = s[0:5]
        #print(s)
        #print(s[6:10])
        #print(s[11:15])
        #print(s[16:20])
        #print(s[21:25])
        #print(cod)
        izarriba = int(s[6:10])
        derarriba = int(s[11:15])
        izabajo = int(s[16:20])
        derabajo = int(s[21:25])
        return
    except:
        izarriba =9999
        derarriba = 9999
        izabajo =9999
        derabajo =9999
        return

numeromensajerecibido=0

def pidedistancia():
    global izarriba
    global derarriba
    global izabajo
    global derabajo
    global firmapaqquete
    global numeromensajerecibido
    nextmsg()
    mensaje = 'L' + firmapaquete + "-"
    try:
        a.write(mensaje)
        return
    except:
        izarriba =9999
        derarriba = 9999
        izabajo =9999
        derabajo =9999
        return
        

def consultadistancia():    
    global izarriba
    global derarriba
    global izabajo
    global derabajo
    global firmapaqquete
    global numeromensajerecibido
    try:
        s=a.read(100).decode()
        cod = s[1:5]
        #print(mensaje)
        #print(cod)
        #print(s)
        numeromensajerecibido=int(s[2:5])
        #print(numeromensajerecibido)
        #print(s[6:10])
        #print(s[11:15])
        #print(s[16:20])
        #print(s[21:25])
        izarriba = int(s[6:10])
        derarriba = int(s[11:15])
        izabajo = int(s[16:20])
        derabajo = int(s[21:25])
        return
    except:
        izarriba =9999
        derarriba = 9999
        izabajo =9999
        derabajo =9999
        return



def leedistancia():
    global izarriba
    global derarriba
    global izabajo
    global derabajo
    global firmapaqquete
    global numeromensajerecibido
    nextmsg()
    mensaje = 'L' + firmapaquete + "-"
    try:
        a.write(mensaje)
        time.sleep_ms(20)
        s=a.read(100).decode()
        cod = s[1:5]
        #print(mensaje)
        #print(cod)
        #print(s)
        numeromensajerecibido=int(s[2:5])
        #print(numeromensajerecibido)
        #print(s[6:10])
        #print(s[11:15])
        #print(s[16:20])
        #print(s[21:25])
        izarriba = int(s[6:10])
        derarriba = int(s[11:15])
        izabajo = int(s[16:20])
        derabajo = int(s[21:25])
        return
    except:
        izarriba =9999
        derarriba = 9999
        izabajo =9999
        derabajo =9999
        return

def verificalectura():
    global firmapaquete
    global numeromensajerecibido   
    if(int(firmapaquete)>numeromensajerecibido):
        print('verifica lectura')
        print (numeromensajerecibido)
        print(int(firmapaquete))
        try:
            s=a.read(100).decode()
            cod = s[1:5]
            numeromensajerecibido=int(s[2:5])
            izarriba = int(s[6:10])
            derarriba = int(s[11:15])
            izabajo = int(s[16:20])
            derabajo = int(s[21:25])
            return
        except:
            izarriba =9999
            derarriba = 9999
            izabajo =9999
            derabajo =9999
            return

hub = PrimeHub()
timer = Timer()
contador = 1
# MOTORES
motor_d= Motor('A')
motor_i= Motor('C')
motor_pair = MotorPair('C', 'A')
motor_pair.set_motor_rotation(3.2 * math.pi,'cm')

# SENSORES
colizq = ColorSensor("F")
coladel = ColorSensor("D")
colder = ColorSensor("B")

#luces y sonido
prueba= False
#valores
negro_normal=30
negro_laterales=32
negro_adelante=20
distancia_obstaculo=40
doble_negro=32
distancia_rescate=180
global s

def update():
    global color_i
    global color_d
    color_i = colizq.get_color()
    color_d = colder.get_color()
    global luz_i
    global luz_a
    global luz_d
    luz_i = colizq.get_reflected_light()
    luz_a = coladel.get_reflected_light()
    luz_d = colder.get_reflected_light()

def doblenegro():
    if colder.get_reflected_light() < doble_negro and colizq.get_reflected_light() < doble_negro and coladel.get_reflected_light() <20:
        motor_pair.stop()
        if prueba == True:
            hub.light_matrix.write('N')
            wait_for_seconds(0.5)
            hub.light_matrix.off()
        motor_pair.move_tank(3,'degrees',left_speed=60, right_speed=60)
        if colder.get_reflected_light() < doble_negro and colizq.get_reflected_light() < doble_negro and coladel.get_reflected_light() <20:
            if prueba == True :
                hub.light_matrix.write('n')
                wait_for_seconds(0.5)
                hub.light_matrix.off()
            motor_pair.move_tank(100,'degrees',left_speed=60, right_speed=60)
        else:
            motor_pair.move_tank(-16,'degrees',left_speed=60, right_speed=60)
def verde():
    if colder.get_color() =='green':
        motor_pair.stop()
        motor_d.run_for_degrees(4)
        if colizq.get_color()== 'green':
            if prueba == True :
                hub.light_matrix.show_image('ARROW_N')
                wait_for_seconds(0.5)
                hub.light_matrix.off()
            giro_180_der()
        else:
            if prueba == True :
                hub.light_matrix.show_image('ARROW_E')
                wait_for_seconds(0.5)
                hub.light_matrix.off()
            motor_pair.move_tank(180,'degrees',left_speed=60, right_speed=60)
            giro_90_derecha()
            motor_pair.move_tank(80,'degrees',left_speed=60, right_speed=60)
            busca_izquierda()
    if colizq.get_color() =='green':
        motor_pair.stop()
        motor_i.run_for_degrees(3)
        if colder.get_color() == 'green':
            if prueba == True :
                hub.light_matrix.show_image('ARROW_S')
                wait_for_seconds(0.5)
                hub.light_matrix.off()
            giro_180_der()
        else:
            if prueba == True :
                hub.light_matrix.show_image('ARROW_W')
                wait_for_seconds(0.5)
                hub.light_matrix.off()
            motor_pair.move_tank(180,'degrees',left_speed=60, right_speed=60)
            giro_90_izquirda()
            motor_pair.move_tank(80,'degrees',left_speed=60, right_speed=60)
            busca_izquierda()
def t_derecha():
    if colder.get_reflected_light() < negro_laterales and coladel.get_reflected_light() < negro_adelante:
        motor_pair.start_tank(0,0)
        if prueba == True :
            hub.light_matrix.write('Td')
            wait_for_seconds(1)
            hub.light_matrix.off()
        motor_pair.move_tank(3,'degrees',left_speed=30, right_speed=30)
        if colder.get_reflected_light() < negro_laterales and coladel.get_reflected_light() < negro_adelante:
            if prueba == True :
                if prueba == True :
                    hub.light_matrix.show_image('YES')
                    wait_for_seconds(1)
                    hub.light_matrix.off()
            motor_pair.move_tank(100,'degrees',left_speed=60, right_speed=60)
        else:
            if prueba == True :
                hub.light_matrix.write('no')
                wait_for_seconds(1)
                hub.light_matrix.off()
            motor_pair.move_tank(-15,'degrees',left_speed=60, right_speed=60)
def t_izquierda():
    if colizq.get_reflected_light() < 32 and coladel.get_reflected_light() < 32:
        motor_pair.start_tank(0,0)
        if prueba == True :
            hub.light_matrix.write('Ti')
            wait_for_seconds(0.5)
            hub.light_matrix.off()
        motor_pair.move_tank(3,'degrees',left_speed=30, right_speed=30)
        if colizq.get_reflected_light() < 32 and coladel.get_reflected_light() < 32:
            if prueba == True :
                hub.light_matrix.show_image('YES')
                wait_for_seconds(1)
                hub.light_matrix.off()
            motor_pair.move_tank(100,'degrees',left_speed=60, right_speed=60)
        else:
            if prueba == True :
                hub.light_matrix.write('no')
                wait_for_seconds(1)
                hub.light_matrix.off()
            motor_pair.move_tank(-15,'degrees',left_speed=60, right_speed=60)
def busca_derecha():
    motor_pair.stop()
    wait_for_seconds(1)
    hub.motion_sensor.reset_yaw_angle()
    if prueba == True :
        hub.light_matrix.write('Cde')
    motor_pair.start_tank(-30,30)
    while (hub.motion_sensor.get_yaw_angle() < -10):
        print(hub.motion_sensor.get_yaw_angle())
    motor_pair.stop()
    motor_pair.start_tank(30,-30)
    while(colder.get_reflected_light() > 30):
        print('sensor derecho')
    motor_pair.stop()
    angle = hub.motion_sensor.get_yaw_angle()

def busca_izquierda():
    motor_pair.stop()
    wait_for_seconds(1)
    hub.motion_sensor.reset_yaw_angle()
    if prueba == True :
        hub.light_matrix.write('Ciz')
    motor_pair.start_tank(30,-30)
    while (hub.motion_sensor.get_yaw_angle() < -10):
        print(hub.motion_sensor.get_yaw_angle())
    motor_pair.stop()
    motor_pair.start_tank(-30,30)
    while(colizq.get_reflected_light() > 30):
        print('sensor izquierdo')
    motor_pair.stop()
    angle = hub.motion_sensor.get_yaw_angle()

def giro_90_izquirda():
    motor_pair.start_tank(0,0)
    wait_for_seconds(1)
    hub.motion_sensor.reset_yaw_angle()
    motor_pair.start_tank(30,-30)
    while (hub.motion_sensor.get_yaw_angle() >-85):
        print(hub.motion_sensor.get_yaw_angle())
    motor_pair.start_tank(0,0)
    if prueba == True :
        hub.speaker.beep(60, 1)
    #wait_for_seconds(1)
    angle = hub.motion_sensor.get_yaw_angle()
    # print('Angulo:', angle)

def giro_90_derecha():
    motor_pair.start_tank(0,0)
    wait_for_seconds(1)
    hub.motion_sensor.reset_yaw_angle()
    motor_pair.start_tank(-30,30)
    while (hub.motion_sensor.get_yaw_angle() < 85):
        print(hub.motion_sensor.get_yaw_angle())
    motor_pair.start_tank(0,0)
    if prueba == True :
        hub.speaker.beep(60, 1)
    # wait_for_seconds(1)
    angle = hub.motion_sensor.get_yaw_angle()
    # print('Angulo:', angle)

def giro_180_der():
    giro_90_izquirda()
    giro_90_izquirda()
    motor_pair.move_tank(0.7,'cm',30,-30)

def giro_180_izq():
    giro_90_derecha()
    giro_90_derecha()
    motor_pair.move_tank(0.7,'cm',-30,30)

def giro_90_derecha_rescate():
    motor_pair.start_tank(0,0)
    wait_for_seconds(1)
    hub.motion_sensor.reset_yaw_angle()
    motor_pair.start_tank(-20,40)
    while (hub.motion_sensor.get_yaw_angle() < 83):
        print(hub.motion_sensor.get_yaw_angle())
    motor_pair.start_tank(0,0)
    if prueba == True :
        hub.speaker.beep(60, 1)
    # wait_for_seconds(1)
    angle = hub.motion_sensor.get_yaw_angle()
    # print('Angulo:', angle)

def giro_90_izquirda_rescate():
    motor_pair.start_tank(0,0)
    wait_for_seconds(1)
    hub.motion_sensor.reset_yaw_angle()
    motor_pair.start_tank(40,-20)
    while (hub.motion_sensor.get_yaw_angle() >-83):
        print(hub.motion_sensor.get_yaw_angle())
    motor_pair.start_tank(0,0)
    if prueba == True :
        hub.speaker.beep(60, 1)
    #wait_for_seconds(1)
    angle = hub.motion_sensor.get_yaw_angle()
    # print('Angulo:', angle)



def rescate_izquierda():
    global esquina
    rescate_v1=0
    leedistancia()
    verificalectura()
    #print(derarriba)
    while rescate_v1 <3:
        motor_pair.start_tank(100,98)
        leedistancia()
        print(leedistancia,)
        verificalectura()
        #print(derarriba)
        while derarriba > distancia_rescate:
            leedistancia()
            print( derarriba , 'izquierda')
        if coladel.get_reflected_light() < 20:
            motor_pair.stop()
            esquina=rescate_v1+2
            motor_pair.move_tank(110, 'degrees', left_speed=-80, right_speed=-80)
            wait_for_seconds(1)
            mueveservoarriba()
            wait_for_seconds(1)
            motor_pair.move_tank(600, 'degrees', left_speed=-80, right_speed=-80)
            motor_pair.stop()
            mueveservoabajo()
            wait_for_seconds(1)
        motor_pair.stop()
        if prueba == True :
            hub.light_matrix.write('Rd')
            wait_for_seconds(1)
            hub.light_matrix.off()
        motor_pair.stop()
        giro_90_derecha_rescate()
        motor_pair.move_tank(800, 'degrees', left_speed=-90, right_speed=-90)
        leedistancia()
        verificalectura()
        #print(derarriba)
        rescate_v1= rescate_v1 + 1
    esquinas_iz()

def rescate_derecha():
    global esquina
    rescate_v1=0
    while rescate_v1 <3:
        motor_pair.start_tank(98,100)
        leedistancia()
        verificalectura()
        #print(derarriba)
        while derarriba > distancia_rescate:
            leedistancia()
            verificalectura()
            print( derarriba , 'derecha')
        if coladel.get_reflected_light() < 20:
            esquina= rescate_v1 +2
            motor_pair.stop()
            motor_pair.move_tank(110, 'degrees', left_speed=-80, right_speed=-80)
            wait_for_seconds(1)
            mueveservoarriba()
            wait_for_seconds(1)
            motor_pair.move_tank(600, 'degrees', left_speed=-80, right_speed=-80)
            motor_pair.stop()
            mueveservoabajo()
            wait_for_seconds(1)
        motor_pair.stop()
        if prueba == True :
            hub.light_matrix.write('Rd')
            wait_for_seconds(1)
            hub.light_matrix.off()
        motor_pair.stop()
        giro_90_izquirda_rescate()
        motor_pair.move_tank(800, 'degrees', left_speed=-90, right_speed=-90)
        leedistancia()
        verificalectura()
        #print(derarriba)
        rescate_v1= rescate_v1 + 1
    esquina_der()

def rescate_inicio():
    global esquina
    motor_pair.stop()
    leedistancia()
    verificalectura()
    #print(derarriba)
    if derarriba < 280:
        motor_pair.stop()
        if prueba == True :
            hub.light_matrix.write('180')
            wait_for_seconds(1)
            hub.light_matrix.off()
        #motor_pair.move_tank(10, 'cm', left_speed=-75, right_speed=-75)
        giro_180_izq()
        motor_pair.move_tank(800, 'degrees', left_speed=-90, right_speed=-90)
        motor_pair.stop()
        leedistancia()
        verificalectura()
        #print(derarriba)
        rescate_izquierda()
        esquinas_iz()
    else:
        motor_pair.stop()
        if prueba == True :
            hub.light_matrix.write('-')
            wait_for_seconds(1)
            hub.light_matrix.off()
        motor_pair.stop()
        wait_for_seconds(0.5)
        motor_pair.move_tank(800, 'degrees', left_speed=-90, right_speed=-90)
        leedistancia()
        verificalectura()
        #print(derarriba)
        rescate_derecha()
        esquina_der()
    angle = hub.motion_sensor.get_yaw_angle()


esquina=1
def esquina_der():
    global esquina_derecha
    if esquina == 1:
        motor_pair.start_tank(100,98)
        leedistancia()
        verificalectura()
        #print(derarriba)
        while derarriba > distancia_rescate:
            leedistancia()
            verificalectura()
            print( derarriba , 'derecha')
        if coladel.get_reflected_light() < 20:
            motor_pair.stop()
            motor_pair.move_tank(110, 'degrees', left_speed=-80, right_speed=-80)
            wait_for_seconds(1)
            mueveservoarriba()
            wait_for_seconds(1)
            motor_pair.move_tank(600, 'degrees', left_speed=-80, right_speed=-80)
            motor_pair.stop()
            mueveservoabajo()
            wait_for_seconds(1)
        motor_pair.stop()
    elif esquina == 2:
        motor_pair.move_tank(650, 'degrees', left_speed=60, right_speed=60)
        motor_pair.stop()
        hub.motion_sensor.reset_yaw_angle()
        motor_pair.start_tank(50,-50)
        while (hub.motion_sensor.get_yaw_angle() > -60):
            a=1
        motor_pair.stop()
        motor_pair.start_tank(100,98)
        leedistancia()
        verificalectura()
        #print(derarriba)
        while derarriba > distancia_rescate:
            leedistancia()
            verificalectura()
            print( derarriba , 'derecha')
        if coladel.get_reflected_light() < 20:
            motor_pair.stop()
            motor_pair.move_tank(110, 'degrees', left_speed=-80, right_speed=-80)
            wait_for_seconds(1)
            mueveservoarriba()
            wait_for_seconds(1)
            motor_pair.move_tank(600, 'degrees', left_speed=-80, right_speed=-80)
            motor_pair.stop()
            mueveservoabajo()
            wait_for_seconds(1)
        motor_pair.stop()
    elif esquina == 3:
        motor_pair.move_tank(2000, 'degrees', left_speed=80, right_speed=80)
        motor_pair.stop()
        hub.motion_sensor.reset_yaw_angle()
        motor_pair.start_tank(50,-50)
        while (hub.motion_sensor.get_yaw_angle() > -120):
            a=1
        motor_pair.stop()
        motor_pair.start_tank(98,100)
        leedistancia()
        verificalectura()
        #print(derarriba)
        while derarriba > distancia_rescate:
            leedistancia()
            verificalectura()
            print( derarriba , 'derecha')
        if coladel.get_reflected_light() < 20:
            motor_pair.stop()
            motor_pair.move_tank(110, 'degrees', left_speed=-80, right_speed=-80)
            wait_for_seconds(1)
            mueveservoarriba()
            wait_for_seconds(1)
            motor_pair.move_tank(600, 'degrees', left_speed=-80, right_speed=-80)
            motor_pair.stop()
            mueveservoabajo()
            wait_for_seconds(1)
        motor_pair.stop()

def esquinas_iz():
    global esquina
    if esquina== 1:
        motor_pair.start_tank(98,100)
        leedistancia()
        verificalectura()
        #print(derarriba)
        while derarriba > distancia_rescate:
            leedistancia()
            verificalectura()
            print( derarriba , 'derecha')
        if coladel.get_reflected_light() < 20:
            motor_pair.stop()
            motor_pair.move_tank(110, 'degrees', left_speed=-80, right_speed=-80)
            wait_for_seconds(1)
            mueveservoarriba()
            wait_for_seconds(1)
            motor_pair.move_tank(600, 'degrees', left_speed=-80, right_speed=-80)
            motor_pair.stop()
            mueveservoabajo()
            wait_for_seconds(1)
        motor_pair.stop()
    elif esquina == 2:
        motor_pair.move_tank(650, 'degrees', left_speed=90, right_speed=90)
        motor_pair.stop()
        hub.motion_sensor.reset_yaw_angle()
        motor_pair.start_tank(-50,50)
        while (hub.motion_sensor.get_yaw_angle() < 60):
            a=1
        motor_pair.stop()
        motor_pair.start_tank(100,100)
        leedistancia()
        verificalectura()
        #print(derarriba)
        while derarriba > distancia_rescate:
            leedistancia()
            verificalectura()
            print( derarriba , 'derecha')
        if coladel.get_reflected_light() < 20:
            motor_pair.stop()
            motor_pair.move_tank(110, 'degrees', left_speed=-90, right_speed=-90)
            wait_for_seconds(1)
            mueveservoarriba()
            wait_for_seconds(1)
            motor_pair.move_tank(600, 'degrees', left_speed=-90, right_speed=-90)
            motor_pair.stop()
            mueveservoabajo()
            wait_for_seconds(1)
        motor_pair.stop()
        motor_pair.move_tank(200, 'degrees', left_speed=-90, right_speed=-90)
    elif esquina == 3:
        motor_pair.move_tank(2000, 'degrees', left_speed=100, right_speed=100)
        motor_pair.stop()
        hub.motion_sensor.reset_yaw_angle()
        motor_pair.start_tank(-50,50)
        while (hub.motion_sensor.get_yaw_angle() < 120):
            a=1
        motor_pair.stop()
        motor_pair.start_tank(98,100)
        leedistancia()
        verificalectura()
        #print(derarriba)
        while derarriba > distancia_rescate:
            leedistancia()
            verificalectura()
            print( derarriba , 'derecha')
        if coladel.get_reflected_light() < 20:
            motor_pair.stop()
            motor_pair.move_tank(110, 'degrees', left_speed=-90, right_speed=-90)
            wait_for_seconds(1)
            mueveservoarriba()
            wait_for_seconds(1)
            motor_pair.move_tank(600, 'degrees', left_speed=-90, right_speed=-90)
            motor_pair.stop()
            mueveservoabajo()
            wait_for_seconds(1)
        motor_pair.stop()

def rescate():
    global esquina_derecha
    global esquina_izquierda
    if coladel.get_green() > 950 and coladel.get_blue() > 950 and coladel.get_red() > 950 :            #izarriba derarriba izabajo derabajo
        motor_pair.stop()
        wait_for_seconds(1)
        mueveservoabajo()
        wait_for_seconds(2)
        motor_pair.start_tank(100,98)
        leedistancia()
        verificalectura()
        while (derarriba > distancia_rescate):
            leedistancia()
            verificalectura()
            #print(derarriba)
        motor_pair.stop()
        if coladel.get_reflected_light() < 20:
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

controlPID = True
tanterior = 0.01
tiempo = 0.01
integral = 0.0
derivada = 0.0
error_previo = 0.0
mueveservoarriba()
wait_for_seconds(1)
cuenta = -1


while True:
    #global cuenta
    global color_i
    global color_d
    global luz_i
    global luz_a
    global luz_d
    cuenta = cuenta + 1
    color_i = colizq.get_color()
    color_d = colder.get_color()
    luz_i = colizq.get_reflected_light()
    luz_a = coladel.get_reflected_light()
    luz_d = colder.get_reflected_light()    
    if cuenta%20 == 0:
        pidedistancia()

    if controlPID == True:
        velocidad = 18
        kp = 1.2    # 3.95 antes
        ki = 0.0    # 0.02 antes
        kd = 0.15   # 0.4antes
        tanterior = tiempo
        tiempo = time.ticks_ms()
        dt = tiempo - tanterior
        error = luz_d - luz_i
        proporcional = error
        integral = integral+ error * 0.005
        derivada = (error - error_previo)
        #    salida = int(kp * proporcional + ki * integral + kd * derivada)
        error_previo = error
        salida = int(kp * proporcional + ki * integral + kd * derivada)
        #print(error, derivada, integral, salida, velocidad + salida, velocidad - salida, dt)
        motor_pair.start_tank(velocidad + salida,velocidad - salida)
    else:
        if colizq.get_reflected_light() > negro_normal:
            motor_d.start_at_power(38)
        else:
            motor_d.start_at_power(-55)
        if colder.get_reflected_light() > negro_normal:
            motor_i.start_at_power(-38)
        else:
            motor_i.start_at_power(55)

    if luz_i < 30 or luz_d < 30 or luz_a < 40 :
        timer.reset()
    
    if timer.now() > 2.5:
        motor_pair.stop()
        motor_pair.start_tank(-30,-30)
        while (colizq.get_reflected_light() > 30 and colder.get_reflected_light() > 30 and coladel.get_reflected_light() > 40):
            print('sin linea')
        motor_pair.stop()
        if colizq.get_reflected_light() < 30:
            motor_d.run_for_degrees(100,-45)
            motor_pair.stop()
        else:
            if colder.get_reflected_light() < 30:
                motor_i.run_for_degrees(100, 45)# bien
                motor_pair.stop()

    verde()
    doblenegro()
    t_derecha()
    t_izquierda()
    rescate()
