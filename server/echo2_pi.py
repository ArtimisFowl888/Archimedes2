import socket

HOST = '192.168.1.42'  # Standard loopback interface address (localhost)
PORT = 21567  # Port to listen on (non-privileged ports are > 1023)
scale = 90

L = 0
R = 0
V = 0
cam = 100
angle = 1000 + cam * 1000 / 180
n = 0
claw = 1000 + cam * 1000 / 180

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()

    def conecct():
        global conn, addr
        conn, addr = s.accept()
        print('Connected by', addr)

    while True:
        global conn, addr
        conecct()
        with conn:

            while True:

                try:
                    Dat = conn.recv(1024).decode("utf-8")
                    data = Dat.split(",")
                except:
                    conecct()

                try:
                    if not Dat:
                        break
                        conecct()
                    if data[9] == 'R':
                        print(data)
                        i = float(data[0])
                        j = float(data[1])
                        k = float(data[2])

                        if (abs(i) < 0.05):
                            i = 0
                        if (abs(j) < 0.05):
                            j = 0
                        if (abs(k) < 0.2):
                            k = 0
                        L = i
                        R = j
                        V = k
                        print(i, j, k, int(data[3]))
                        if int(data[5]) == 1:
                            angle = angle + 0.15
                        if int(data[6]) == 1:
                            angle = angle - 0.15
                        if (angle < 1200):
                            angle = 1200
                        if (angle > 2000):
                            angle = 2000

                        if int(data[3]) == 1:
                            claw = claw + 0.15
                        if int(data[4]) == 1:
                            claw = claw - 0.15
                        if (claw < 1200):
                            claw = 1200
                        if (claw > 2000):
                            claw = 2000
                        # pi.set_servo_pulsewidth(23,angle)
                        #
                        #
                        # c.L(L*scale)
                        # c.R(R*scale)
                        # c.LV(V*scale)
                        # c.RV(V*scale)

                        data2 = str('%2.2f,%2.2f,%2.2f,%2.2f,%2.2f' % (L * scale, R * scale, V * scale, angle, claw))
                        conn.sendall(data2.encode("utf-8"))
                except:
                    continue
