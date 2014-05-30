__author__ = 'JordSti'

from socket import *
from game import *
import threading
import sys

connection_id = 1

def get_connection_id():
    global connection_id
    cid = connection_id
    connection_id += 1
    return cid


class connection(threading.Thread):

    def __init__(self, client, master):
        threading.Thread.__init__(self)

        self.connection_id = get_connection_id()
        self.master = master
        self.client = client
        self.buffer_size = 1024
        self.connected = True

    def remove(self):
        self.master.threads.remove(self)

    def run(self):
        print "Connection #%d" % self.connection_id
        try:
            welcome_msg = "Welcome to %s !\n" % self.master.name
            password_needed = False
            if self.master.password is not None:
                welcome_msg += "Password needed for this server\n"
                password_needed = True
            self.client.send(welcome_msg)

            if password_needed:
                req = self.client.recv(self.buffer_size)
                req = req.rstrip('\n')

                if req == self.master.password:
                    #password is good
                    #todo
                    print "Password is ok !"
                    self.client.send("Success\n")
                else:
                    self.client.send("Invalid password\nClosing Connection\n")
                    self.client.close()
                    self.remove()
                    self.connected = False

        except IOError as e:
            self.connected = False
            print "IO Error [%s: %s]" % (e.errno, e.strerror)
            self.remove()

        while self.connected:
            request = self.client.recv(self.buffer_size)

            if len(request) == 0:
                self.client.close()
            else:
                print request


class game_thread(threading.Thread):

    def __init__(self, context=game_context()):
        threading.Thread.__init__(self)
        self.context = context
        self.game = game_object(context)

    def run(self):
        self.game.start_game()


class game_server:

    def __init__(self, name="SqConquerer", port=4050, max_players=4, password=None):
        self.name = name
        self.port = port
        self.max_players = max_players
        self.password = password
        self.threads = []
        self.bind_socket = socket(AF_INET, SOCK_STREAM)
        self.run = True

    def start_server(self):
        print "Starting server and listening on %d" % self.port
        self.bind_socket.bind(('127.0.0.1', self.port))

        while self.run:
            try:
                self.bind_socket.listen(5)

                (client, addr) = self.bind_socket.accept()

                print "Accepting connection from %s:%d" % (addr[0], addr[1])

                client_thread = connection(client, self)

                self.threads.append(client_thread)
                client_thread.start()

            except IOError as e:
                print "IOError [%s: %s]" % (e.errno, e.strerror)

#
# main section
#

if __name__ == "__main__":
    print "SqConquerer server"

    port = 4050
    password = None
    name = "SqConquerer"

    ia = 0
    ma = len(sys.argv)

    while ia < ma:
        arg = sys.argv[ia]

        if arg == '-p' or arg == '--port':
            ia += 1
            if ia < ma:
                port = int(sys.argv[ia])
        elif arg == '-k' or arg == '--key':
            ia += 1
            if ia < ma:
                password = sys.argv[ia]
        elif arg == '-n' or arg == '--name':
            ia += 1
            if ia < ma:
                name = sys.argv[ia]

        ia += 1

    server = game_server(name, port, 4, password)
    server.start_server()