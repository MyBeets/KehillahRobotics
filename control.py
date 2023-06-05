import socket
import serial
import msvcrt
import time
TCP_IP = "localhost"
TCP_PORT = 8080
BUFFER_SIZE = 32

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
arduino = serial.Serial(port='COM4', baudrate=9600, timeout=5)#.01

s.connect((TCP_IP, TCP_PORT))
while True:
    data = s.recv(BUFFER_SIZE)
    arduino.write(data)
    #arduino.write(bytes('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'utf-8'))#bytes(data, 'utf-8')
    # print(bytes("hello", 'utf-8'))
    print("received data: ", data.decode("latin-1"))
    # line = arduino.read(BUFFER_SIZE)#BUFFER_SIZE
    # print("HERE:",line," next ",data)
    # if str(line) != "b''":
    #     print("line",line)
    if msvcrt.kbhit():
        if str(msvcrt.getch()) == "b'q'":
            break
s.close()