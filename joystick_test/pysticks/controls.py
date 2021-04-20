import socket
from sys import stdout

import pygame


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 21567  # The port used by the server

# Initialize pygame for joystick support
pygame.display.init()
pygame.joystick.init()
controller = pygame.joystick.Joystick(0)
controller.init()


while True:
    # Get next pygame event
    pygame.event.pump()
    y = controller.get_axis(1)
    x = controller.get_axis(0)
    L = -y + x
    R = -y - x
    v = -controller.get_axis(3)
    g1 = controller.get_button(0)
    g2 = controller.get_button(1)
    c5u = controller.get_button(4)
    c5d = controller.get_button(2)
    c1u = controller.get_button(5)
    c1d = controller.get_button(3)
    d = str('%2.2f,%2.2f,%2.2f,%x,%x,%x,%x,%x,%x,R' % (L, R, v, g1, g1, c5u, c5d, c1u, c1d))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(d.encode("utf-8"))
        data = s.recv(1024).decode("utf-8")
        print('Received', repr(data))
        s.close()