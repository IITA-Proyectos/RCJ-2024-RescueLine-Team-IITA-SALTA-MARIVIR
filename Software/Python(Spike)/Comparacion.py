from spike import PrimeHub, LightMatrix, Button, StatusLight,MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor
from spike.control import wait_for_seconds, wait_until, Timer
from spike import MotorPair
import hub
import time
import math
import random
from utime import sleep_ms, ticks_ms
import sys, os

connection = hub.USB_VCP()
connection.init(flow=hub.USB_VCP.CTS | hub.USB_VCP.RTS)
connection.setinterrupt(-1)
primeHub = PrimeHub()
timer = Timer()
contador = 1
# engine
right_engine= Motor('C')
left_engine= Motor('A')
motor_pair = MotorPair('C', 'A')
motor_pair.set_motor_rotation(3.2 * math.pi,'cm')

# # color sensor
left_color = ColorSensor("B")
forward_color = ColorSensor("D")
right_color = ColorSensor("F")

#luces y sonido
proof= False
#valores
basic_blak_color=75 #30 /70
side_black_color=50# 29 / 50
black_color_front=65 #20
double_blck=52#32/52

global rgb_red, rgb_blue, rgb_green, rgb_red_a, rgb_blue_a, rgb_green_a
rgb_red=0
rgb_blue=0
rgb_green=0
rgb_red_a = 0
rgb_blue_a = 0
rgb_green_a = 0
global distancia_frente, distancia_izquierda, distancia_derecha
distancia_frente =240
distancia_izquierda =240
distancia_derecha = 240
#pitch =primeHub.motion_sensor.get_pitch_angle()
parar = False
modo = "linea"
rampa=0
cuenta_rescate=0
def update():
    global color_l, color_r, light_l, light_f, light_r, rgb_red, rgb_blue, rgb_green, rgb_red_a, rgb_blue_a, rgb_green_a
    global sensor_arduino, distancia_frente, distancia_izquierda, distancia_derecha
    global pitch

    color_l = left_color.get_color()
    color_r = right_color.get_color()

    light_l = left_color.get_reflected_light()
    light_f = forward_color.get_reflected_light()
    light_r = right_color.get_reflected_light()

    rgb_red = forward_color.get_red()
    rgb_green = forward_color.get_green()
    rgb_blue = forward_color.get_blue()
    if connection.any():
        received_data = connection.read(1)
        if received_data is not None:
            if received_data < b'\xf0': # Esto es el 240
                distancia_frente = str(received_data[0])
    pitch =primeHub.motion_sensor.get_pitch_angle()

    # Aquí deberíamos agregar la lectura del pitch
def update_arduino():
# connection.write("<<X>>")
    if connection.any():
        received_data = connection.read(1)
        if received_data is not None:
            # received_data = received_data
            if received_data == b'\xff': # Esto es el 255
                global parar
                parar = True
            if received_data == b'\xfe': # Esto es el 254
                parar = False
            if received_data == b'\xfd': # Esto es el 253
                rgb_red_a_data = connection.read(1)
                if rgb_red_a_data  is not None:
                    rgb_red_a= str(rgb_red_a_data[0]) # to extract the right value
                    primeHub.speaker.beep(50, 1)
                    # try:
                    #     if int(rgb_red_a_data) < 10:
                    #         primeHub.speaker.beep(90, 0.1)
                    # except:
                    #     pass
            if received_data == b'\xfc': # Esto es el 252
                rgb_green_a = connection.read(1)
                if rgb_green_a_data is not None:
                    rgb_green_a= str(rgb_green_a_data[0]) # to extract the right value
                    primeHub.speaker.beep(50,1)
                    # try:
                    #     if int(rgb_green_a_data) < 10:
                    #         primeHub.speaker.beep(90, 0.1)
                    # except:
                    #     pass
            if received_data == b'\xfb': # Esto es el 251
                rgb_blue_a = connection.read(1)
                if rgb_blue_a_data is not None:
                    rgb_blue_a= str(rgb_blue_a_data[0]) # to extract the right value
                    primeHub.speaker.beep(50,1)
                    # try:
                    #     if int(rgb_blue_a_data) < 10:
                    #         primeHub.speaker.beep(90, 0.1)
                    # except:
                    #     pass
            if received_data == b'\xfa': # Esto es el 250 << Lo que sigue es --> sensor_ultrasonido_izquierda >>
                distancia_izquierda_data = connection.read(1)
                if distancia_izquierda_data is not None:
                    distancia_izquierda = str(distancia_izquierda_data[0]) # to extract the right value
                    primeHub.speaker.beep(50, 1)
                    # try:
                    #     if int(distancia_izquierda) < 10:
                    #         primeHub.speaker.beep(90, 5)
                    # except:
                    #     pass
            if received_data == b'\xf9': # Esto es el 249 << Lo que sigue es --> sensor_ultrasonido_derecha >>
                sensor_derecha_data = connection.read(1)
                if sensor_derecha_data is not None:
                    distancia_derecha = str(sensor_derecha_data[0]) # to extract the right value
                    primeHub.speaker.beep(50,1)
                    # try:
                    #     if int(distancia_derecha) < 10:
                    #         primeHub.speaker.beep(90, 5)
                    # except:
                    #     pass
            if received_data == b'\xf8': # Esto es el 248 << Lo que sigue es --> sensor_ultrasonido_frente >>
                distancia_frente_data = connection.read(1)
                if distancia_frente_data is not None:
                    distancia_frente = str(distancia_frente_data[0]) # to extract the right value
                    """
                    try:
                        if int(distancia_derecha) < 20:
                            primeHub.speaker.beep(90, 0.1)
                    except:
                        pass
                    """
            if received_data < b'\xf0': # Esto es el 240
                distancia_frente = str(received_data[0])
                """
                try:
                    if int(distancia_frente) < 10:# Aparently the values mean is << 3unit --> 5cm >>
                        #primeHub.speaker.beep(90, 0.5)
                        primeHub.light_matrix.show_image('BUTTERFLY')
                except:
                    pass
                """


def non_blocking_wait_ms(wait_time_ms):
    global parar
    start_time=ticks_ms()
    while (ticks_ms() - start_time) < wait_time_ms and not parar:
        update()
        update_arduino()

commandHeaderAndAddress = "55AA11"

algorithmsByteID = {
    "ALGORITHM_OBJECT_TRACKING": "0100",
    "ALGORITHM_FACE_RECOGNITION": "0000",
    "ALGORITHM_OBJECT_RECOGNITION": "0200",
    "ALGORITHM_LINE_TRACKING": "0300",
    "ALGORITHM_COLOR_RECOGNITION": "0400",
    "ALGORITHM_TAG_RECOGNITION": "0500",
    "ALGORITHM_OBJECT_CLASSIFICATION": "0600",
    "ALGORITHM_QR_CODE_RECOGNITION" : "0700",
    "ALGORITHM_BARCODE_RECOGNITION":"0800",
}


class Arrow:
    def __init__(self, xTail, yTail , xHead , yHead, ID):
        self.xTail=xTail
        self.yTail=yTail
        self.xHead=xHead
        self.yHead=yHead
        self.ID=ID
        self.learned= True if ID > 0 else False
        self.type="ARROW"


class Block:
    def __init__(self, x, y , width , height, ID):
        self.x = x
        self.y=y
        self.width=width
        self.height=height
        self.ID=ID
        self.learned= True if ID > 0 else False
        self.type="BLOCK"

class HuskyLensCamera:
    def __init__(self, port = 0, baudrate = 9600, debug=True):
        self.checkOnceAgain=True
        self.DEBUG=debug
        self.unprocessed_data=b''
        self.baudrate = baudrate
        self.reads_per_ms = 10

        if type(port) == str:
            self.uart = eval("primeHub.port."+port)
        else:
            self.uart = port
        self.uart.mode(1)
        #non_blocking_wait_ms(300)
        sleep_ms(300)
        self.uart.baud(baudrate)
        #non_blocking_wait_ms(200)
        sleep_ms(200)
        self.lastCmdSent = ""
        self.flush()
        self.knock()

    def force_read(self, size=1, timeout=50):
        data = b''
        r = self.uart.read(1)
        for i in range(timeout*self.reads_per_ms):
            if r==None:
                r=b''
            data += r
            if len(data) == size:
                return data
            else:
                r=self.uart.read(1)
            #if i > 3 and self.DEBUG:
            #    print("Waiting for data in force read...")
        return data

    def available(self):
        self.unprocessed_data=self.force_read(1, timeout=1)
        if self.unprocessed_data==None:
            self.unprocessed_data=b''
        return len(self.unprocessed_data)

    def read_all(self):
        # Read full receive buffer
        available = self.available()
        data = self.unprocessed_data
        self.unprocessed_data = b''
        while True:
            r=self.uart.read(1)
            if r==b'': break
            data += r
        return data

    def read(self, n = 1):
        if n==0:
            return b''
        data = self.force_read(n, timeout=2)
        if data==None:
            data=b''
        return data

    def flush(self):
        _ = self.read_all()
        if self.DEBUG: print("Flushed: %r" % _)

    def writeToHuskyLens(self, msg):
        window = 32
        if self.DEBUG: print("Sending %r" % msg)
        while len(msg) > window:
            self.uart.write(msg[:window])
            non_blocking_wait_ms(5)
            msg = msg[window:]
        self.uart.write(msg)
        #self.flush()

    def calculateChecksum(self, hexStr):
        total = 0
        for i in range(0, len(hexStr), 2):
            total += int(hexStr[i:i+2], 16)
        hexStr = hex(total)[-2:]
        return hexStr

    def convert_to_class_object(self,data,isBlock):
        tmp=[]
        for i in data:
            if(isBlock):
                obj = Block(i[0],i[1],i[2],i[3],i[4])
            else:
                obj = Arrow(i[0],i[1],i[2],i[3],i[4])
            tmp.append(obj)
        return tmp

    def knock(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002c3c")
        self.writeToHuskyLens(cmd)
        non_blocking_wait_ms(5)
        return self.processReturnData()

    def blocks(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002131")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def algorithm(self, alg):
        if alg in algorithmsByteID:
            cmd = commandHeaderAndAddress+"022d"+algorithmsByteID[alg]
            cmd += self.calculateChecksum(cmd)
            cmd = self.cmdToBytes(cmd)
            self.writeToHuskyLens(cmd)
            non_blocking_wait_ms(200)
            return self.processReturnData()
        else:
            print("INCORRECT ALGORITHM NAME")

    def learn(self,x):
        data = "{:04x}".format(x)
        part1=data[2:]
        part2=data[0:2]
        #reverse to correct endiness
        data=part1+part2
        dataLen = "{:02x}".format(len(data)//2)
        cmd = commandHeaderAndAddress+dataLen+"36"+data
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def forget(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"003747")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def setCustomName(self,name,idV):
        nameDataSize = "{:02x}".format(len(name)+1)
        #name = name.encode("utf-8").hex()+"00"
        name = ''.join(self.bytesToHex(name.encode('utf-8')))+'00'
        localId = "{:02x}".format(idV)
        data = localId+nameDataSize+name
        dataLen = "{:02x}".format(len(data)//2)
        cmd = commandHeaderAndAddress+dataLen+"2f"+data
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def customText(self,nameV,xV,yV):
        #name=nameV.encode("utf-8").hex()
        name = ''.join(self.bytesToHex(nameV.encode('utf-8')))
        nameDataSize = "{:02x}".format(len(name)//2)
        if(xV>255):
            x="ff"+"{:02x}".format(xV%255)
        else:
            x="00"+"{:02x}".format(xV)
        y="{:02x}".format(yV)

        data = nameDataSize+x+y+name
        dataLen = "{:02x}".format(len(data)//2)

        cmd = commandHeaderAndAddress+dataLen+"34"+data
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def clearText(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"003545")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def requestAll(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002030")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def saveModelToSDCard(self,idVal):
        idVal = "{:04x}".format(idVal)
        idVal = idVal[2:]+idVal[0:2]
        cmd = commandHeaderAndAddress+"0232"+idVal
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def loadModelFromSDCard(self,idVal):
        idVal = "{:04x}".format(idVal)
        idVal = idVal[2:]+idVal[0:2]
        cmd = commandHeaderAndAddress+"0233"+idVal
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def savePictureToSDCard(self):
        self.uart.timeout=5
        cmd = self.cmdToBytes(commandHeaderAndAddress+"003040")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def saveScreenshotToSDCard(selxf):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"003949")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def arrows(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002232")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()[0]

    def learned(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002333")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()[0]

    def learnedBlocks(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002434")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()[0]

    def learnedArrows(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002535")
        self.writeToHuskyLens(cmd)
        return self.processReturnData()[0]

    def getObjectByID(self, idVal):
        idVal = "{:04x}".format(idVal)
        idVal = idVal[2:]+idVal[0:2]
        cmd = commandHeaderAndAddress+"0226"+idVal
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()[0]

    def getBlocksByID(self, idVal):
        idVal = "{:04x}".format(idVal)
        idVal = idVal[2:]+idVal[0:2]
        cmd = commandHeaderAndAddress+"0227"+idVal
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()

    def getArrowsByID(self, idVal):
        idVal = "{:04x}".format(idVal)
        idVal = idVal[2:]+idVal[0:2]
        cmd = commandHeaderAndAddress+"0228"+idVal
        cmd += self.calculateChecksum(cmd)
        cmd = self.cmdToBytes(cmd)
        self.writeToHuskyLens(cmd)
        return self.processReturnData()[0]

    def count(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002030")
        self.writeToHuskyLens(cmd)
        return len(self.processReturnData())

    def learnedObjCount(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002030")
        self.writeToHuskyLens(cmd)
        return self.processReturnData(numIdLearnFlag=True)[-1]

    def frameNumber(self):
        cmd = self.cmdToBytes(commandHeaderAndAddress+"002030")
        self.writeToHuskyLens(cmd)
        return self.processReturnData(frameFlag=True)[-1]


    def cmdToBytes(self, cmd):
        # https://stackoverflow.com/questions/47727170/difference-between-bytes-fromhex-and-encode
        #return bytes.fromhex(cmd)
        return bytes(int(cmd[i:i + 2], 16) for i in range(0, len(cmd), 2))

    def bytesToHex(self, buf):
        return list('{0:02x}'.format(int(buf[i]), 16) for i in range(0, len(buf)))

    def splitCommandToParts(self, cmd):
        #print("cmd: %s" % cmd)
        headers = cmd[0]+cmd[1]
        address = cmd[2]
        data_length = int(cmd[3], 16) # decode base 16 int
        command = cmd[4]
        if(data_length > 0):
            data = ''.join(cmd[5:5+data_length])
        else:
            data= []
        checkSum = cmd[-1] # bug

        return [headers, address, data_length, command, data, checkSum]

    def getBlockOrArrowCommand(self):
        byteString = self.force_read(5)
        byteString += self.force_read(byteString[3])
        byteString += self.uart.read(1)
        byteStringHex = self.bytesToHex(byteString)
        if self.DEBUG: print ("get block returned: %r" % byteStringHex)
        commandSplit = self.splitCommandToParts(byteStringHex)
        isBlock = True if commandSplit[3] == "2a" else False
        return (commandSplit[4],isBlock)

    def processReturnData(self, numIdLearnFlag=False, frameFlag=False):
        byteString = b''
        try:
            byteString = self.force_read(5)
            byteString += self.force_read(byteString[3])
            byteString += self.force_read(1)

            if self.DEBUG: print ("Returned: %r" % byteString)
            byteStringHex = self.bytesToHex(byteString)
            if self.DEBUG: print ("as hex list: %r" % byteStringHex)
            commandSplit = self.splitCommandToParts(byteStringHex)
            if self.DEBUG: print("command split: %r" % commandSplit)
            chk = self.calculateChecksum(''.join(byteStringHex[:-1]))
            if self.DEBUG: print("calc checksum:", chk)
            if (chk != commandSplit[-1]):
                print("checksum error")
                return []

            cmdType = commandSplit[3]
            if(cmdType == "2e"):
                # self.checkOnceAgain=True
                if self.DEBUG: print("COMMAND_RETURN_OK")
                self.flush()
                return "OK"
            else:
                if (cmdType == "29") and self.DEBUG:
                    print ("COMMAND_RETURN_INFO")
                returnData = []
                numberOfBlocksOrArrow = int( commandSplit[4][2:4]+commandSplit[4][0:2], 16 )
                numberOfIDLearned = int( commandSplit[4][6:8]+commandSplit[4][4:6], 16 )
                frameNumber = int( commandSplit[4][10:12]+commandSplit[4][8:10], 16 )
                if self.DEBUG:print("qty:",numberOfBlocksOrArrow)
                if self.DEBUG:print("nID:", numberOfIDLearned)
                if self.DEBUG: print("frm:", frameNumber)

                isBlock=True
                for i in range(numberOfBlocksOrArrow):
                    #if self.DEBUG: print("getting block ", i)
                    tmpObj=self.getBlockOrArrowCommand()
                    isBlock=tmpObj[1]
                    returnData.append(tmpObj[0])

                finalData = []
                tmp = []
                # print(returnData)
                for i in returnData:
                    tmp = []
                    for q in range(0, len(i), 4):
                        low=int(i[q:q+2], 16)
                        high=int(i[q+2:q+4], 16)
                        if(high>0):
                            val=low+255+high
                        else:
                            val=low
                        tmp.append(val)
                    finalData.append(tmp)
                    tmp = []
                self.checkOnceAgain=True
                ret=self.convert_to_class_object(finalData,isBlock)
                if(numIdLearnFlag):
                    ret.append(numberOfIDLearned)
                if(frameFlag):
                    ret.append(frameNumber)
                return ret

        except Exception as exc:
            print("EXCEPTION : "+str(exc))
            if(self.checkOnceAgain):
                #self.uart.timeout=5
                self.checkOnceAgain=False
                #self.uart.timeout=.5
                return self.processReturnData()
            print("Read response error, please try again")
            self.flush()
            return []

#####################################################################################################################################################################################
##########################################################################PROGRAMA SEGUIDOR DE LINEA###############################################################################################
#####################################################################################################################################################################################
def doubleblack():
    if light_r < double_blck and light_l < double_blck :
        motor_pair.stop()
        if proof == True:
            primeHub.light_matrix.write('N')
            non_blocking_wait(1)
            primeHub.light_matrix.off()
        motor_pair_move_tank_update(10,'degrees',60,60)
        if right_color.get_reflected_light() < double_blck and left_color.get_reflected_light() < double_blck:
            if proof == True :
                primeHub.light_matrix.write('n')
                non_blocking_wait(1)
                primeHub.light_matrix.off()
            motor_pair_move_tank_update(55,'degrees',60,60)
        else:
            motor_pair_move_tank_update(16,'degrees',-60,-60)

def green():# deteccion de verdes
    if color_r =='green':
        motor_pair_move_tank_update(4,'degrees',20,25)
        if left_color.get_color()== 'green': #comprobacion del doble verde
            if proof == True :
                primeHub.light_matrix.show_image('ARROW_N')
                non_blocking_wait(1)
                primeHub.light_matrix.off()
            turn_180_rigth()
            look_left_line()
        else: # verde para un lado
            if proof == True :
                primeHub.light_matrix.show_image('ARROW_W')
                primeHub.light_matrix.off()
                non_blocking_wait(1)
            motor_pair_move_tank_update(80,'degrees',40,40)
            turn_90_right()
            motor_pair_move_tank_update(85,'degrees',45,45)
            look_left_line()
    if color_l =='green': # deteccion del doble verde
        motor_pair_move_tank_update(4,'degrees',25,20)
        if right_color.get_reflected_light() == 'green':
            if proof == True :
                primeHub.light_matrix.show_image('ARROW_N')
                non_blocking_wait(0.5)
                primeHub.light_matrix.off()
            turn_180_rigth()
            look_left_line()
        else:# verde de un solo lado
            if proof == True :
                primeHub.light_matrix.show_image('ARROW_E')
                non_blocking_wait(0.5)
                primeHub.light_matrix.off()
            motor_pair_move_tank_update(80,'degrees',40,40) #45 - 60
            turn_90_left()
            motor_pair_move_tank_update(85,'degrees',45,45)
            look_left_line()

def right_intersection():
    if light_r < side_black_color and light_f < black_color_front:
        motor_pair.start_tank(0,0)
        if proof == True :
            primeHub.light_matrix.write('Td')
            non_blocking_wait(1)
            primeHub.light_matrix.off()
        motor_pair_move_tank_update(8,'degrees',40,40)
        if right_color.get_reflected_light() < side_black_color and forward_color.get_reflected_light() < black_color_front:# comprueba que sea una interseccion real
            if proof == True :
                if proof == True :
                    primeHub.light_matrix.show_image('YES')
                    non_blocking_wait(1)
                    primeHub.light_matrix.off()
            motor_pair_move_tank_update(50,'degrees',60,60)
        else: # vuelve a su posicion original hacia atras, detecto que es falso lo que leyo
            if proof == True :
                primeHub.light_matrix.write('no')
                non_blocking_wait(1)
                primeHub.light_matrix.off()
            motor_pair_move_tank_update(15,'degrees',-60,-60)

def left_intersection():
    if light_l < side_black_color and light_f< black_color_front:
        motor_pair.start_tank(0,0)
        if proof == True :
            primeHub.light_matrix.write('Ti')
            non_blocking_wait(0.5)
            primeHub.light_matrix.off()
        motor_pair_move_tank_update(8,'degrees',40,40)
        if left_color.get_reflected_light() < side_black_color and forward_color.get_reflected_light() < black_color_front:
            if proof == True :
                primeHub.light_matrix.show_image('YES')
                non_blocking_wait(1)
                primeHub.light_matrix.off()
            motor_pair_move_tank_update(50,'degrees',60,60)
        else:
            if proof == True :
                primeHub.light_matrix.write('no')
                non_blocking_wait(1)
                primeHub.light_matrix.off()
            motor_pair_move_tank_update(15,'degrees',-60,-60)

def obstaculo():
    global distancia_frente,distancia_derecha, distancia_izquierda
    if 1 <= int(distancia_frente) <= 5: # fix the value 10 to detect with raw byte
        ##### código para recibir por el arduino
        #primeHub.speaker.beep(90, 0.1)
        motor_pair.stop()
        non_blocking_wait(1)
        if distancia_derecha >= distancia_izquierda:
            motor_pair_move_tank_update(50,'degrees',-40,-40)
            turn_90_right()
            motor_pair.start_tank(90,20)
            while( left_color.get_reflected_light() > 30 and not parar):
                update()
            motor_pair.start_tank(0,0)
            non_blocking_wait(1)
            turn_90_right()
        elif distancia_derecha <= distancia_izquierda:
            motor_pair_move_tank_update(50,'degrees',-40,-40)
            turn_90_left()
            motor_pair.start_tank(20,90)
            while( left_color.get_reflected_light() > 30 and not parar):
                update()
            motor_pair.start_tank(0,0)
            non_blocking_wait(2)
            turn_90_left()
        """else:
            giro_alatorio = random.randint(1, 2)
            if giro_alatorio == 1:
                motor_pair_move_tank_update(50,'degrees',-40,-40)
                turn_90_right()
                motor_pair.start_tank(90,20)
                while( left_color.get_reflected_light() > 30 and not parar):
                    update()
                motor_pair.start_tank(0,0)
                non_blocking_wait(2)
                turn_90_right()
            else:
                motor_pair_move_tank_update(50,'degrees',-40,-40)
                turn_90_left()
                motor_pair.start_tank(20,90)
                while( left_color.get_reflected_light() > 30 and not parar):
                    update()
                motor_pair.start_tank(0,0)
                non_blocking_wait(2)
                turn_90_left()"""

def motor_pair_move_tank_update(cantidad,tipo,velocidad_izquierda,velocidad_derecha):
    motor_pair.stop()
    right_engine.set_degrees_counted(0)
    motor_pair.start_tank(velocidad_izquierda,velocidad_derecha)
    while (abs(right_engine.get_degrees_counted()) < cantidad and not parar ):
        update()
        update_arduino()
    motor_pair.stop()




def look_rigth_line():
    global parar
    motor_pair.stop()
    non_blocking_wait(1)
    primeHub.motion_sensor.reset_yaw_angle()
    if proof == True :
        primeHub.light_matrix.write('Cde')
    motor_pair.start_tank(-30,30)
    while (primeHub.motion_sensor.get_yaw_angle() < -10 and not parar):
        update()
        #print(primeHub.motion_sensor.get_yaw_angle())
    motor_pair.stop()
    motor_pair.start_tank(30,-30)
    while(right_color.get_reflected_light() >basic_blak_color and not parar):
        update()
        #print('sensor derecho')
    motor_pair.stop()
    angle = primeHub.motion_sensor.get_yaw_angle()

def look_left_line():
    global parar
    motor_pair.stop()
    non_blocking_wait(1)
    primeHub.motion_sensor.reset_yaw_angle()
    if proof == True :
        primeHub.light_matrix.write('Ciz')
    motor_pair.start_tank(30,-30)
    while (primeHub.motion_sensor.get_yaw_angle() <10 and not parar):
        update()
    motor_pair.stop()
    motor_pair.start_tank(-30,30)
    while(left_color.get_reflected_light() > basic_blak_color and not parar):
        update()
        #print('sensor izquierdo')
    motor_pair.stop()
    angle = primeHub.motion_sensor.get_yaw_angle()

def turn_90_left():
    global parar
    motor_pair.start_tank(0,0)
    non_blocking_wait(1)
    primeHub.motion_sensor.reset_yaw_angle()
    motor_pair.start_tank(40,-40)
    while (primeHub.motion_sensor.get_yaw_angle() <75 and not parar):# 85
        update()
        # print(primeHub.motion_sensor.get_yaw_angle())
    motor_pair.start_tank(0,0)
    if proof == True :
        primeHub.speaker.beep(60, 1)
    #non_blocking_wait(1)
    angle = primeHub.motion_sensor.get_yaw_angle()
    # print('Angulo:', angle)

def turn_90_right():
    global parar
    motor_pair.start_tank(0,0)
    non_blocking_wait(1)
    primeHub.motion_sensor.reset_yaw_angle()
    motor_pair.start_tank(-40,40)
    while (primeHub.motion_sensor.get_yaw_angle() >-75 and not parar):#85
        update()
        # print(primeHub.motion_sensor.get_yaw_angle())
    motor_pair.start_tank(0,0)
    if proof == True :
        primeHub.speaker.beep(60, 1)
    # non_blocking_wait(1)
    angle = primeHub.motion_sensor.get_yaw_angle()
    # print('Angulo:', angle)

def turn_180_rigth():
    turn_90_left()
    turn_90_left()
    motor_pair_move_tank_update(10,'degrees',40,40)

def turn_180_left():
    turn_90_right()
    turn_90_right()
    motor_pair_move_tank_update(10,'degrees',40,40)

############################################################################################################################################################################################
###########################################################################RESCATE##############################################################################################################################
#########################################################################################################################################################################################################
def motor_pair_move_tank_update_rescate(cantidad,tipo,velocidad_izquierda,velocidad_derecha):
    motor_pair.stop()
    right_engine.set_degrees_counted(0)
    motor_pair.start_tank(velocidad_izquierda,velocidad_derecha)
    while (abs(right_engine.get_degrees_counted()) < cantidad and not parar ):
        Aproximity()
        #asd = 1
        update_arduino() 
    motor_pair.stop()


def turn_90_right_rescue():
    motor_pair.start_tank(0, 0)
    #non_blocking_wait(1)
    primeHub.motion_sensor.reset_yaw_angle()
    motor_pair.start_tank(-20, 40)
    while primeHub.motion_sensor.get_yaw_angle() < 83 and not parar:
        Aproximity()
        update_arduino()
    motor_pair.start_tank(0, 0)
    if proof:
        primeHub.speaker.beep(60, 1)
    angle = primeHub.motion_sensor.get_yaw_angle()
    # print('Angulo:', angle)


def turn_90_left_rescue():
    motor_pair.start_tank(0,0)
    #non_blocking_wait(1)
    primeHub.motion_sensor.reset_yaw_angle()
    motor_pair.start_tank(40,-20)
    while primeHub.motion_sensor.get_yaw_angle() >-83 and not parar:
        Aproximity()
        update_arduino()
    motor_pair.start_tank(0,0)
    if proof == True :
        primeHub.speaker.beep(60, 1)
    angle = primeHub.motion_sensor.get_yaw_angle()

def turn_45_rigth_rescue():
    motor_pair.start_tank(0,0)
    non_blocking_wait(1)
    primeHub.motion_sensor.reset_yaw_angle()
    motor_pair.start_tank(-10,30)
    while primeHub.motion_sensor.get_yaw_angle() > -45 and not parar:
        Aproximity()
        update_arduino()
    motor_pair.start_tank(0,0)
    if proof == True :
        primeHub.speaker.beep(60, 1)
    angle = primeHub.motion_sensor.get_yaw_angle()

def turn_45_left_rescue(): # Revisar
    motor_pair.stop()
    non_blocking_wait(1)
    primeHub.motion_sensor.reset_yaw_angle()
    motor_pair.start_tank(30, -10)
    while primeHub.motion_sensor.get_yaw_angle() < 45 and not parar:
        Aproximity()
        update_arduino()
    motor_pair.start_tank(0,0)
    if proof == True :
        primeHub.speaker.beep(60, 1)
    angle = primeHub.motion_sensor.get_yaw_angle()

def turn_180_rescue_rigth():
    #connection.write("<<M>>>")
    motor_pair_move_tank_update_rescate(99,"degrees",20,80)
    #motor_pair.stop()
    #right_engine.set_degrees_counted(int(0))
    #motor_pair.start_tank(10,40)
    #while ((abs(right_engine.get_degrees_counted())) < 1800 and not parar ):
    #    update_arduino()
        #Aproximity()
    #motor_pair.stop()
    # motor_pair.stop()
    # non_blocking_wait(1)
    # primeHub.speaker.beep(89,1)
    # motor_pair.start_tank(-10,30)
    # start = time.ticks_ms()
    # while time.ticks_diff(time.ticks_ms(), start) <1500 and not parar:
    #    Aproximity()
    #    update_arduino()
    # primeHub.speaker.beep(99,1)
    # start=0
    # motor_pair.stop()

def turn_180_rescue_left():
    #connection.write("<<M>>>")
    motor_pair_move_tank_update_rescate(99,"degrees",80,20)
    # motor_pair.stop()
    # right_engine.set_degrees_counted(int(0))
    # motor_pair.start_tank(40,10)
    # while ((abs(right_engine.get_degrees_counted())) < 1800 and not parar ):
    #     update_arduino()
    #     #Aproximity()
    # motor_pair.stop()
    # motor_pair.stop()
    # non_blocking_wait(1)
    # primeHub.speaker.beep(89,1)
    # motor_pair.start_tank(30,-10)
    # start = time.ticks_ms()
    # while time.ticks_diff(time.ticks_ms(), start) <1500 and not parar:
    #    Aproximity()
    #    update_arduino()
    # primeHub.speaker.beep(99,1)
    # start=0
    # motor_pair.stop()

def Aproximity():
    #motor_pair.stop()
    ball = huskyLens.getBlocksByID(1)
    if proof == True:
        primeHub.speaker.beep(90, 1)
    victima=0
    if len(ball) == 1:
        FollowVictim()
        if proof == True:
            primeHub.speaker.beep(100, 1)
        motor_pair.stop()
        non_blocking_wait(1)
        if proof == True:
            primeHub.speaker.beep(60,1)
        victima += 1

# def avanza_mirando():
#     motor_pair.move_tank_update("degree",20,20)

    # motor_pair.stop()
    # right_engine.set_degrees_counted(0)
    # motor_pair.start_tank(40,40)
    # while (abs(right_engine.get_degrees_counted()) < 250 and not parar ):
    #     update_arduino()
    # motor_pair.stop()


def cuadrado_izquierdo():
    motor_pair_move_tank_update_rescate(700,'degrees',80,80)
    primeHub.speaker.beep(99, 1)
    motor_pair_move_tank_update_rescate(200,"degrees",80,20)



    #--------------- Segundo giro de prueba ---------------------------
    #motor_pair_move_tank_update(100, "degrees", 70, 30)
    #primeHub.speaker.beep(99, 1)


    # #Aproximity()
    # update_arduino()
    # turn_180_rescue_left()
    # #motor_pair_move_tank_update(20,"degrees",20,20)
    # #non_blocking_wait(2)
    # #avanza_mirando()
    # primeHub.speaker.beep(90, 1)

def cuadrado_derecho():
    motor_pair_move_tank_update_rescate(700,'degrees',80,80)
    primeHub.speaker.beep(99, 1)
    motor_pair_move_tank_update_rescate(200,"degrees",20,80)
   

    #--------------- Segundo giro de prueba ---------------------------
    #motor_pair_move_tank_update(100, "degrees", 30, 70)
    #primeHub.speaker.beep(99, 1)


    # #Aproximity()
    # update_arduino()
    # turn_180_rescue_rigth()
    # #motor_pair_move_tank_update(20,"degree",20,20)
    # #non_blocking_wait(2)
    # #avanza_mirando()
    # primeHub.speaker.beep(90, 1)

def pared():
    if int(distancia_izquierda) < int(distancia_derecha): #sensor ultrasnido derecho
        turn_45_rigth_rescue()
        cuadrado_derecho()
    elif int(distancia_izquierda) > int(distancia_derecha):
        turn_45_left_rescue()
        cuadrado_izquierdo()
    else:
        primeHub.speaker.beep(50, 0.1)
        giro_alatorio = random.randint(1, 2)
        if giro_alatorio == 1:
            cuadrado_derecho()
        else:
            cuadrado_izquierdo()

# Revisar funciones de cuadrado !!

def rescate():
    # if rgb_green() > 630 and rgb_blue() > 700 and rgb_red() > 620:
    motor_pair.stop()
    motor_pair_move_tank_update(200, "degrees", 95,95)  
    motor_pair.stop()
    non_blocking_wait(3)
    pared()

def FollowVictim():
    global victima_muerta
    global victima_viva
    victima_viva=0
    victima_muerta = 0
    while True:
        vivo = huskyLens.getBlocksByID(1)
        if len(vivo) == 1:
            x_position = vivo[0].x
            h_height = vivo[0].height
            if x_position < 150:# Si el objeto está a la izquierda del eje X
                # motor_pair.move(1, "cm", steering=100)
                motor_pair_move_tank_update(15, "degrees",0,15)

            elif x_position > 180:# Si el objeto está a la derecha del eje X
                # motor_pair.move(0.5, "cm", steering=-100)

                motor_pair_move_tank_update(15, "degree",15,0)
            else:
                if x_position > 170 and x_position < 180:
                    if x_position > 170:
                        motor_pair.start(20, 15)
                    else:
                        if x_position < 170:
                            motor_pair.start(15,20)
                        else:
                            motor_pair.start(40, 40)
                else:
                    motor_pair_move_tank_update(15, "degrees",-15,-15)
                    if h_height > 65:
                        motor_pair_move_tank_update(200,"degrees",15,15)
                        motor_pair.stop()
                        non_blocking_wait(1)
                        connection.write("<<A>>")
                        non_blocking_wait(7)
                        if 105 <=int(rgb_red_a) <= 110 and 48<=int(rgb_blue_a) <=52 and 44<= int(rgb_green_a)<= 48:# plateado
                            connection.write("<<D>>")
                            non_blocking_wait(5)
                            victima_viva +=1
                            depositar()
                        elif 105<=int(rgb_red_a)<= 110 and 48<=int(rgb_blue_a)<=52 and 44<= int(rgb_green_a)<= 48:# negro
                            connection.write("<<E>>")
                            non_blocking_wait(5)
                            victima_muerta=1
                            #depositar()
                        else:
                            pared()
                            #mayor_ultrasonido()
        else:
            #motor_pair.move_tank(1, "cm", left_speed=15, right_speed= 15)
            pared()
def depositar():
    if victima_viva >=1:
        motor_pair.start(80,80)
        while(1<distancia_frente <10):
            update_arduino()
            Aproximity()
        motor_pair.stop()
        if distancia_derecha < distancia_izquierda :
            turn_90_left_rescue()
            motor_pair.start(90, 90)
            while( 1<=distancia_frente<=10):
                update_arduino()
                Aproximity()
            motor_pair.stop()
            motor_pair_move_tank_update(10, "degrees",-60,80)
            if 16 < int(rgb_red_a) < 28 and 22< int(rgb_blue_a)< 39 and 27<int(rgb_green_a)< 48: #verde
                if victima_plateada >= 1:
                    turn_180_left()
                    motor_pair.stop()
                    motor_pair_move_tank_update(20, "degrees",-90,-90)
                    connection.write("<<F>>")
                    motor_pair_move_tank_update(15, "degrees",-90,-90)
                    motor_pair_move_tank_update(5, "degrees",90,90)
                    motor_pair_move_tank_update(15, "degrees",-90,-90)
            elif 94<int(rgb_red_a)< 230 and 33<int(rgb_blue_a) <86 and 29< int(rgb_green_a)< 75:#rojo
                if victima_muerta>=1:
                    turn_180_left()
                    motor_pair.stop()
                    motor_pair_move_tank_update(20, "degrees",-90,-90)
                    connection.write("<<F>>")
                    motor_pair_move_tank_update(15, "degrees",-90,-90)
                    motor_pair_move_tank_update(5, "degrees", 90,90)
                    motor_pair_move_tank_update(15, "degrees",-90,-90)
            else:
                turn_90_rigth_rescue()
                motor_pair.start(90, 90)
                while( 1<distancia_frente<10):
                    update_Arduino()
                    Aproximity()
                motor_pair_move_tank_update(10, "degrees",-60,80)
        if distancia_derecha > distancia_izquierda:
            turn_90_right_rescue()
            motor_pair.start(90, 90)
            while( 1<distancia_frente<10):
                update_arduino()
                Aproximity()
            motor_pair.stop()
            motor_pair_move_tank_update(10, "degrees",-60,80)
            if 40 < int(rgb_red_a) < 45 and 70< int(rgb_blue_a)< 76 and 85<int(rgb_green_a)< 90: #verde
                if victima_plateada >=1:
                    turn_180_left()
                    motor_pair.stop()
                    motor_pair_move_tank_update(20, "degrees", -90,-90)
                    connection.write("<<F>>")
                    motor_pair_move_tank_update(15, "degrees",-90,-90)
                    motor_pair_move_tank_update(5, "degrees",90,90)
                    motor_pair_move_tank_update(15, "degrees",-90,-90)
            elif 105<int(rgb_red_a)< 110 and 48<int(rgb_blue_a) <52 and 44< int(rgb_green_a)< 48:#rojo
                if victima_muerta >= 1:
                    turn_180_left()
                    motor_pair.stop()
                    motor_pair_move_tank_update(20, "degrees",-90,-90)
                    connection.write("<<F>>")
                    motor_pair_move_tank_update(15, "degrees",-90,-90)
                    motor_pair_move_tank_update(5, "degrees",90,90)
                    motor_pair_move_tank_update(15, "degrees",-90,-90)
            else:
                turn_90_rigth_rescue()
                motor_pair.start(90, 90)
                while( 1<distancia_frente<10):
                    update_arduino()
                    Aproximity()
                motor_pair_move_tank_update(10, "degrees",-60,80)


huskyLens = HuskyLensCamera(hub.port.E, baudrate = 9600, debug= False)
display = LightMatrix()
#########################################################################################################################################################################################
#################################################################################### MAIN CODE ##########################################################################################
#########################################################################################################################################################################################
cuenta=0

tanterior = 0.01
tiempo = 0.01
integral = 0.0
derivada = 0.0
error_previo = 0.0
cuenta = -1
kp = 1.7# 3.95 antes
ki = 0    # 0.02 antes
kd = 0.4# 0.4antes /0.15


# Creo que estos valores deberiamos leerlos por primera vez

# parar = False
# modo = "rescate"
# pitch = 0
# data_claw_normal = True
# data_claw_ramp = True

def non_blocking_wait(wait_time):
    global parar
    start_time = time.time()
    while (time.time() - start_time) < wait_time and not parar:
        update()
        update_arduino()

def non_blocking_si_parar(wait_time):
    global parar
    start_time=time.time()
    while(time.time() - start_time) < wait_time and parar:
        update()
        update_arduino()

non_blocking_wait(2)
connection.write("<<T>>")
#primeHub.light_matrix.write('T')

while True:
    global rgb_red, rgb_green, rgb_blue, rgb_red_a, rgb_green_a, rgb_blue_a
    update()
    currentMillis = time.time()

    if parar == True and modo != "stop":
        motor_pair.stop()
        # primeHub.speaker.beep(50, 0.5)
        modo = "stop"
        connection.write("<<S>>") # #Send data to arduino << S: confirm stop mode to arduino>>

    if modo == "stop":
        primeHub.light_matrix.write('R')
        non_blocking_si_parar(1)
        primeHub.light_matrix.off()
        non_blocking_si_parar(1)

    if parar == False and modo == "stop":
        modo = "linea"
        connection.write("<<O>>") #Send data to arduino << O: line mode in arduino>>
        motor_pair.start_tank(15,15)
        non_blocking_wait(1)

    if modo == "linea":
        if pitch > 6:
            if rampa == 1:
                connection.write("<<M>>")
                rampa= 0
            #print("abajo")
            velocidad= 12
            tanterior = tiempo
            tiempo = ticks_ms()
            dt = tiempo - tanterior
            error = light_r - light_l
            proporcional = error
            integral = integral+ error * 0.005
            derivada = (error - error_previo)
            #salida = int(kp * proporcional + ki * integral + kd * derivada)
            error_previo = error
            salida = int(kp * proporcional + ki * integral + kd * derivada)
            #print(error, derivada, integral, salida, velocidad + salida, velocidad - salida, dt)
            vderecha = velocidad + salida
            if vderecha < 10:
                vderecha = vderecha - 50
            vizquierda = velocidad - salida
            if vizquierda < 10:
                vizquierda = vizquierda - 50
            motor_pair.start_tank(vderecha,vizquierda)
        elif pitch == 0:
            if rampa==0:
                connection.write("<<L>>")#Send data to arduino << L: claw in normal mode in arduino>>
                rampa= 1
            #print("Normal")
            velocidad=12#15
            tanterior = tiempo
            tiempo = ticks_ms()
            dt = tiempo - tanterior
            error = light_r - light_l
            proporcional = error
            integral = integral+ error * 0.005
            derivada = (error - error_previo)
            #    salida = int(kp * proporcional + ki * integral + kd * derivada)
            error_previo = error
            salida = int(kp * proporcional + ki * integral + kd * derivada)
            #print(error, derivada, integral, salida, velocidad + salida, velocidad - salida, dt)
            vderecha = velocidad + salida
            if vderecha < 5:
                vderecha = vderecha - 10
            vizquierda = velocidad - salida
            if vizquierda < 5 :
                vizquierda = vizquierda - 10
            motor_pair.start_tank(vderecha,vizquierda)
        elif pitch <-5:
            if rampa==1:
                connection.write("<<M>>")
                rampa= 0
            # print("arriba")
            velocidad=40
            tanterior = tiempo
            tiempo = ticks_ms()
            dt = tiempo - tanterior
            error = light_r - light_l
            proporcional = error
            integral = integral+ error * 0.005
            derivada = (error - error_previo)
            #    salida = int(kp * proporcional + ki * integral + kd * derivada)
            error_previo = error
            salida = int(kp * proporcional + ki * integral + kd * derivada)
            #print(error, derivada, integral, salida, velocidad + salida, velocidad - salida, dt)
            vderecha = velocidad + salida
            vizquierda = velocidad - salida
            motor_pair.start_tank(vderecha,vizquierda)
        if light_l < basic_blak_color or light_r < basic_blak_color or light_f <black_color_front : #dan los de los costados menos de 35 el de adelante menos de 25
            timer.reset()
        if timer.now() > 3:
            motor_pair.stop()
            motor_pair.start_tank(-25,-25)
            while light_l >60 and light_r > 60 :
                update()
            motor_pair.stop()
            if light_l < 30:
                motor_pair_move_tank_update(10, "degrees",30,0)
                motor_pair.stop()
            else:
                if light_r < 30:
                    motor_pair_move_tank_update(10, "degrees",0,30)
                    motor_pair.stop()
        update()
        if int(rgb_green) >900 and int(rgb_blue) >900 and int(rgb_red) >900:
            motor_pair.stop()
            modo= "rescate"
            connection.write("<<R>>")
        obstaculo()
        green()
        doubleblack()
        right_intersection()
        left_intersection()
    if modo == "rescate":
        rescate()
