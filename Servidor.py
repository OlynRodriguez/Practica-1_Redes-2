import socket
import os

HOST = input("Ingresa una IP destino: ")
PORT = int(input("Ingresa un Puerto: "))
buffer_size = 1024
casilla1 = ''
casilla2 = ''

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
    print("Conectando con el servidor.")
    clientSocket.connect((HOST, PORT))
    print("**Conexion establecida**")
    # DEFINIENDO DIFICULTAD
    dificultad = input("--MENU--\n1.- Facil\n2.- Dificil\nOpcion: ")
    clientSocket.send(dificultad.encode('utf8'))
    os.system("cls")
    if dificultad == '1':
        limite = 3
    else:
        limite = 4

    while True:
        data = clientSocket.recv(buffer_size).decode('utf8')
        if data == '1' or data == '2':
            break
        elif data == '3':
            clientSocket.send('blowjob4'.encode('utf8'))
            data = clientSocket.recv(buffer_size).decode('utf8')
            print(data)
            input('Presiona enter...')
            os.system('cls')
            clientSocket.send('blowjob3'.encode('utf8'))

        elif data == '4':
            print('---Tu turno---')
            clientSocket.send('blowjob4'.encode('utf8'))
            print('Turno del jugador\n\n')
            data = clientSocket.recv(buffer_size).decode('utf8')
            print(data)
            while True:
                casilla1 = input('Selecciona la casilla 1(x,y): ')
                aux = casilla1.split(',')
                if (int(aux[0]) <= limite) and (int(aux[1]) <= limite):
                    break

            clientSocket.send(casilla1.encode('utf8'))
            data = clientSocket.recv(buffer_size).decode('utf8')
            os.system('cls')
            print(data)
            while True:
                casilla2 = input('Seleccione la casilla 2(x,y): ')
                aux = casilla2.split(',')
                if (int(aux[0]) <= limite) and (int(aux[1]) <= limite):
                    break

            clientSocket.send(casilla2.encode('utf8'))
            data = clientSocket.recv(buffer_size).decode('utf8')
            os.system('cls')
            print(data)
            input('Presiona enter..')
            clientSocket.send('xxx'.encode('utf8'))
            os.system('cls')
            data = clientSocket.recv(buffer_size).decode('utf8')
            print(data)
            input("Presiona enter para continuar..")
            clientSocket.send("blowjob".encode('utf8'))
            os.system("cls")

    if data == '1':
        print("GANASTE")
    else:
        print("LA COMPUTADORA GANO")