#python robots class
import serial,math,string,time,msvcrt
wheelSpeeds=[5,5]
 
class Myrobot:
    def __init__(self, speed = 9600, port=0, stopbits=2):
        self.speed = speed
        self.port = port
        self.stopbits = stopbits
        
    #Connect the robot
    def connect(self):  
        " connects the serial port "
        self.serial = serial.Serial(baudrate=self.speed, port=self.port, stopbits=self.stopbits)
        self.serial.open()
        print(self.serial.isOpen())
        print(self.serial)
        print(self.serial.parity)
        self.serial.write("G,0,0\n")
        print(self.serial.readline())
    
    #Disconnect the robot
    def disconnect(self):
        self.serial.close()
    
    #Reset the position counter
    def reset(self):
        self.serial.write("G,0,0\n")
        print(self.serial.readline())
        
    #Read the position counter
    def readPos(self):
        self.serial.write("H\n")
        print(self.serial.readline())
 
    #Set the speed of wheel in mm/sec, range is 0<speed<=1000 mm/sec
    def move(self,leftSpeed,rightSpeed):
        leftSpeed=(leftSpeed*127)/1000
        rightSpeed=(rightSpeed*127)/1000
        command = "D,"+str(leftSpeed)+","+str(rightSpeed)+"\n"
        self.serial.write(command)
        self.serial.readline()
        self.serial.write("E \n")
        self.serial.readline()

    #Let robot move forward indefinitely
    def moveForward(self):
        command="D,"+str(wheelSpeeds[0])+","+str(wheelSpeeds[1])+"\n"
        self.serial.write(command)
        self.serial.readline()
 
    #Let robot move backword indefinitely
    def moveBackward(self):
        commmand="D,-"+str(wheelSpeeds[0])+",-"+str(wheelSpeeds[1])+"\n"
        self.serial.write(command)
        self.serial.readline()

    #Makes robot move forward n millimeters, the range is 0<distance<=670000mm
    def moveForwardDistance(self,distance):
        self.reset()
        rotations=(distance*1000)/80       
        leftCounter=rotations
        rightCounter=rotations
        command="C,"+str(leftCounter)+","+str(rightCounter)+"\n"
        self.serial.write(command)
        self.serial.readline()
        print(str(leftCounter) + " " + str(rightCounter))

    #Make robot move backward n millimeters, the range is 0<distance<=670000mm
    def moveBackwardDistance(self,distance):
        self.reset()
        rotations=(distance*1000)/80
        leftCounter=-rotations
        rightCounter=-rotations
        command="C,"+str(leftCounter)+","+str(rightCounter)+"\n"
        self.serial.write(command)
        self.serial.readline()
        print(str(leftCounter) + " " + str(rightCounter))

    #Make robot stop
    def stop(self):
        command="D,0,0\n"
        self.serial.write(command)
        self.serial.readline()

    #Make robot turn an amount of degrees to the left
    def turnLeft(self,degree):
        self.reset()
        counter=(1035*degree)/180
        if((float(1035*degree)/180)>=90):
            counter=counter+1
            leftCounter=-counter
            rightCounter=counter
            self.serial.write("D,0,0\n")
            self.serial.readline()
            command="C,"+str(leftCounter)+","+str(rightCounter)+"\n"
            self.serial.write(command)
            self.serial.readline()
            print(str(leftCounter) + " " + str(rightCounter))
   
    #Make robot turn an amount of degrees to the right
    def turnRight(self,degree):
        self.reset()
        counter=(1035*degree)/180
        if((float(1035*degree)/180)>=90):
            counter=counter+1
            leftCounter=counter
            rightCounter=-counter
            self.serial.write("D,0,0\n")
            self.serial.readline()
            command="C,"+str(leftCounter)+","+str(rightCounter)+"\n"
            self.serial.write(command)
            self.serial.readline()
            print(str(leftCounter) + " " + str(rightCounter))
   
    #Read the speeds of wheels.
    def wheelSpeeds(self):
        self.serial.write("E\n")
        reply=self.serial.readline()
        rawdata=string.split(reply,",")
        speeds=[]
        for i in range(2):
            speeds.append(string.atoi(rawdata[i+1]))
            print(speeds[i])
 
    #Read the values of each of eight light sensors
    def readLightSensors(self):
        self.serial.write("O\n")
        reply=self.serial.readline()
        self.LightSensors=string.split(reply,",")
        print(self.LightSensors)
        for i in range(8):
            self.LightSensors[i]=string.atoi(self.LightSensors[i+1])
        return self.LightSensors

    #Display the value of requested sensor as numbered
    def getLightSensor(self,s):
        print self.LightSensors[s]
        return self.LightSensors[s]

    #Read the values of each of eight proximity sensors.
    def readProxSensors(self):
        self.serial.write("N\n")
        reply=self.serial.readline()
        self.ProxSensors=string.split(reply,",")
        print(self.ProxSensors)
        for i in range(8):
            self.ProxSensors[i]=string.atoi(self.ProxSensors[i+1])
        return self.ProxSensors
    
    #Display the value of requested sensor as numbered
    def getProxSensor(self,t):
        print self.ProxSensors[t]
        return self.ProxSensors[t]

if __name__ == '__main__':
    r=Myrobot()
    r.connect()
    while not msvcrt.kbhit():
        r.moveForwardDistance(100)
        time.sleep(1)
    r.stop()
    r.disconnnect()