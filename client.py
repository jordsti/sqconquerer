__author__ = 'JordSti'
from socket import *

import sys
from SqException import *

#
# game client class
#

class game_client:
    def __init__(self, address, port=4050, name='johndoe', password=None):
        self.address = address
        self.port = port
        self.name = name
        self.password = password
        self.server = None
        self.buffer_size = 1024

    def connect(self):
        try:
            self.server = socket(AF_INET, SOCK_STREAM)
            self.server.connect((self.address, self.port))
            print "Connected to %s:%d" % (self.address, self.port)
            msg = self.server.recv(self.buffer_size)

            lines = msg.split('\n')

            print lines[0]

            if len(lines) >= 2:
                if 'Password needed' in lines[1]:

                    self.server.send(self.password+'\n')

                    resp = self.server.recv(self.buffer_size)

                    if "Success" in resp:
                        print "Password is ok !"
                    else:
                        raise GameClientException(10, "Incorrect Password")

        except IOError as e:
            print "IOError (%s: %s)" % (e.errno, e.strerror)

#
#main section
#

if __name__ == '__main__':

    host = '127.0.0.1'
    port = 4050
    key = None
    player_name = 'johndoe'

    ia = 0
    ma = len(sys.argv)

    while ia < ma:
        arg = sys.argv[ia]

        if arg == '-p' or arg == '--port':
            ia += 1
            if ia < ma:
                port = int(sys.argv[ia])
        elif arg == '-h' or arg == '--hostname':
            ia += 1
            if ia < ma:
                host = sys.argv[ia]
        elif arg == '-k' or arg == '--key':
            ia += 1
            if ia < ma:
                key = sys.argv[ia]
        elif arg == '-n' or arg == '--name':
            ia += 1
            if ia < ma:
                player_name = sys.argv[ia]

        ia += 1

    client = game_client(host, port, player_name, key)

    client.connect()