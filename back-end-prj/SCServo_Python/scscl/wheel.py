#!/usr/bin/env python
#
# *********     Gen Write Example      *********
#
#
# Available SCServo model on this example : All models using Protocol SCS
# This example is tested with a SCServo(SCS), and an URT
#

import sys
import os

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
        
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

sys.path.append("..")
from scservo_sdk import *                 # Uses SCServo SDK library

# Default setting
SCS_ID                      = 55                 # SCServo ID : 1
BAUDRATE                    = 1000000           # SCServo default baudrate : 1000000
# DEVICENAME                  = '/dev/ttyUSB0'    # Check which port is being used on your controller
DEVICENAME                  = 'COM4'      # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"
SCS_MOVING_SPEED0           = 100         # SCServo moving speed
SCS_MOVING_SPEED1           = -100        # SCServo moving speed

index = 0
scs_move_speed = [SCS_MOVING_SPEED0, 0, SCS_MOVING_SPEED1, 0]

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Get methods and members of Protocol
packetHandler = scscl(portHandler)
    
# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

scs_comm_result, scs_error = packetHandler.PWMMode(SCS_ID)
if scs_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(scs_comm_result))
elif scs_error != 0:
    print("%s" % packetHandler.getRxPacketError(scs_error))  
while 1:
    # print("Press any key to continue! (or press ESC to quit!)")
    # if getch() == chr(0x1b):
    #      break

    print("Press read or write to continue! (or press ESC to quit!)")
    operation = input('please in put \'w\'to write, \'r\' to read , \'s\' to status ')
    print('input operation :',operation)
    if operation == chr(0x1b):
        break


    # Write SCServo goal position/moving speed/moving acc
    print(scs_move_speed[index])
    #scs_comm_result, scs_error = packetHandler.WritePWM(SCS_ID, scs_move_speed[index])
    scs_comm_result, scs_error = packetHandler.WritePWMbyTime(SCS_ID, scs_move_speed[index])
    if scs_comm_result != COMM_SUCCESS:
        print("1%s" % packetHandler.getTxRxResult(scs_comm_result))
    if scs_error != 0:
        print("0%s" % packetHandler.getRxPacketError(scs_error))

    # Change move speed
    index += 1
    if index == 4:
        index = 0

# Close port
portHandler.closePort()
