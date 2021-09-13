import socket
import random
class jugador:
    puntos = 0

    def __init__(self, nombre):
        self.nombre = nombre

class memorama:
    cont: int

    def __init__(self, dificultad):
        self.dificultad = dificultad
        if dificultad == "1":
            self.tablero = [['rojo', 'verde', 'verde', 'azul'],
                            ['amarillo', 'rosa', 'rosa', 'rojo'],
                            ['morado', 'amarillo', 'morado', 'naranja'],
                            ['azul', 'naranja', 'blanco', 'blanco']]
            self.tablero_inv = [['', '', '', ''],
                                ['', '', '', ''],
                                ['', '', '', ''],
                                ['', '', '', '']]
            self.cont = 8
            print("Principiante")
        elif dificultad == "2":
            self.tablero = [['azul', 'verde', 'azul', 'rojo', 'verde', 'rosa'],
                            ['rosa', 'rojo', 'naranja', 'amarillo', 'amarillo', 'dorado'],
                            ['naranja', 'dorado', 'blanco', 'cafe', 'blanco', 'cafe'],
                            ['gris', 'marino', 'gris', 'limon', 'marino', 'limon'],
                            ['negro', 'negro', 'guinda', 'plateado', 'guinda', 'plateado'],
                            ['pink', 'blue', 'pink', 'red', 'blue', 'red']]
            self.tablero_oculto = [['', '', '', '', '', ''],
                                   ['', '', '', '', '', ''],
                                   ['', '', '', '', '', ''],
                                   ['', '', '', '', '', ''],
                                   ['', '', '', '', '', ''],
                                   ['', '', '', '', '', '']]
            self.cont = 18
            print("Avanzado")
        else:
            print("Nada que ver: ", dificultad)

    def mostrar_tablero(self):
        for i in self.tablero_oculto:
            print(i)

    def turno_jugador(self, socket, jugador):
        socket.send('4'.encode('utf8'))
        socket.recv(1024).decode('utf8')
        game.enviar_tablero(Client_conn)
        tirada1 = socket.recv(1024).decode('utf8').split(',')
        print("TIRADA 1")
        x1 = int(tirada1[0])
        y1 = int(tirada1[1])
        self.tablero_oculto[x1][y1] = self.tablero[x1][y1]
        self.enviar_tablero(socket)
        tirada2 = socket.recv(1024).decode('utf8').split(',')
        print("TIRADA 2")
        x2 = int(tirada2[0])
        y2 = int(tirada2[1])
        self.tablero_oculto[x2][y2] = self.tablero[x2][y2]
        self.enviar_tablero(socket)

        if self.tablero[x1][y1] != self.tablero[x2][y2]:
            self.tablero_oculto[x1][y1] = '*'
            self.tablero_oculto[x2][y2] = '*'
        else:
            self.cont -= 1
            jugador.puntos += 1
        socket.recv(1024).decode('utf8')
        self.enviar_tablero(
            socket)
        socket.recv(1024).decode('utf8')
        print("Termina el turno")

    def tirada_pc(self, jugador, conn):
        while True and self.cont != 0:
            while True:
                try:
                    if self.dificultad == "1":
                        x1 = x2 = random.randrange(0, 4)
                        y1 = y2 = random.randrange(0, 4)
                    else:
                        x1 = x2 = random.randrange(0, 5)
                        y1 = y2 = random.randrange(0, 5)
                    if self.tablero_oculto[x1][y1] != '*':
                        x1 = int("/")
                    self.tablero_oculto[x1][y1] = self.tablero[x1][y1]
                    break
                except ValueError:
                    pass
                except IndexError:
                    pass

            while ((x1 == x2) and (y1 == y2)):
                while True:
                    try:
                        if self.dificultad == "1":
                            x2 = random.randrange(0, 4)
                            y2 = random.randrange(0, 4)
                        else:
                            x2 = random.randrange(0, 6)
                            y2 = random.randrange(0, 6)
                        if self.tablero_oculto[x2][y2] != '*':
                            x2 = int("/")
                        self.tablero_oculto[x2][y2] = self.tablero[x2][y2]
                        break
                    except ValueError:
                        pass
                    except IndexError:
                        pass
            conn.send('3'.encode('utf8'))
            conn.recv(1024).decode('utf8')
            self.enviar_tablero(conn)
            conn.recv(1024)
            if self.tablero[x1][y1] != self.tablero[x2][y2]:
                self.tablero_oculto[x1][y1] = '*'
                self.tablero_oculto[x2][y2] = '*'
                break
            else:
                self.cont -= 1
                jugador.puntos += 1
            self.enviar_tablero(conn)
            print('tirada pc')

    def enviar_tablero(self, socket_oirgen):
        text = self.tablero_oculto.__str__().replace('], [', '\n').replace('[[', '').replace(']]', '')
        socket_oirgen.send(text.encode('utf8'))

if __name__ == "__main__":
    HOST = input("Insertar IP del servidor: ")
    PORT = int(input("Inserte el PUERTO: "))
    buffer_size = 8
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
        serverSocket.bind((HOST, PORT))
        while True:
            serverSocket.listen()
            print("El server está disponible y esperando solicitudes")

            Client_conn, Client_addr = serverSocket.accept()
            with Client_conn:
                pc = jugador("pc")
                player = jugador("player")
                print("Conectado a", Client_addr)

                data = Client_conn.recv(1024).decode("utf8")

                game = memorama('data')
                i = 1
                while game.cont:
                    i = 1 - i
                    if i == 0:
                        print('jugador: {}'.format(player.puntos))
                        game.turno_jugador(Client_conn, player)
                    else:
                        print('pc: {}'.format(pc.puntos))
                        game.tirada_pc(pc, Client_conn)
                if player.puntos > pc.puntos:
                    Client_conn.send('1'.encode('utf-8'))
                else:
                    Client_conn.send('2'.encode('utf-8'))