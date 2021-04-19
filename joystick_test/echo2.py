#!/usr/bin/env python3

import socket
from sys import stdout

import pygame


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432  # The port used by the server

# Initialize pygame for joystick support
pygame.display.init()
pygame.joystick.init()
controller = pygame.joystick.Joystick(0)
controller.init()


while True:
    # Get next pygame event
    pygame.event.pump()

    a = str('%s | Axes: ' % controller.get_name())
    for k in range(controller.get_numaxes()):
        b= str('%d:%+2.2f ' % (k, controller.get_axis(k)))
    stdout.write(' | Buttons: ')
    for k in range(controller.get_numbuttons()):
        c = str('%d:%d ' % (k, controller.get_button(k)))
    d = a + b +c
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(d.encode())
        data = s.recv(1024)
        print('Received', repr(data))
