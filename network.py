__author__ = 'JordSti'

from SqException import *
import re

request_id = 0

def get_request_id():
    global request_id

    rid = request_id

    request_id += 1

    return rid


class network_field:

    (Integer, Float, String, List) = (0, 1, 2, 3)

    def __init__(self, name="", data="", field_type=String):
        self.name = name
        self.data = data
        self.field_type = field_type

    def to_string(self):

        data = ""

        if self.field_type == self.Integer:
            data = "i%d" % self.data
        elif self.field_type == self.Float:
            #need a test on this !! todo
            data = "f%d" % self.data
        elif self.field_type == self.String:
            data = "%s"
        elif self.field_type == self.List:
            raise Exception(0, "Not Implemented")

        return "%s:%s;" (self.name, data)

    def from_string(self, text):
        text = text.rstrip(";")
        data = text.split(":")

        if len(data) >= 2:
            self.name = data[0]

            val = data[1]

            #int pattern
            ipattern = re.compile("i(<int>[0-9]+)")

            #float pattern
            fpattern = re.compile("f(<float>[0-9]+\\.|,?[0-9]*)")
            #need test on this regex

            m = ipattern.match(val)

            if m:
                data = int(m.group("int"))
                self.field_type = self.Integer
            else:
                m = fpattern.match(val)

                if m:
                    data = float(m.group("float"))
                    self.field_type = self.Float
                else:
                    data = val
                    self.field_type = self.String

            self.data = data

        else:
            raise ParsingException(201002, "Error parsing network field")


class network_object:

    def __init__(self, data=""):
        self.data = data
        self.sended = False
        self.received = False
        self.buffer_size = 2048

    def to_data(self):
        pass

    def from_data(self):
        pass

    def send(self, target_socket):
        self.to_data()
        try:
            target_socket.send(self.data)
            self.sended = True
        except IOError as e:
            print "IOError (%d: %s)" (e.errno, e.strerror)

    def receive(self, source_socket):

        try:
            self.data = source_socket.recv(self.buffer_size)
            self.from_data()
            self.received = True
        except IOError as e:
            print "IOError (%d: %s)" (e.errno, e.strerror)

    def length(self):
        return len(self.data)

class request(network_object):

    def __init__(self, command, args=[], r_id=get_request_id()):
        request.__init__(self)
        self.request_id = r_id
        self.command = command
        self.args = args

    def to_data(self):
        args = ""

        for a in self.args:
            args += "%s," % a

        args = args.rstrip(",")

        data = "%d - %s (%s)" % (self.request_id, self.command, args)

        self.data = data

    def from_data(self):

        pattern = re.compile("(<id>[0-9]+) - (<command>[a-z0-9_\\-]) \\((<args>.*)\\)")

        m = pattern.match(self.data)

        if m:
            self.request_id = int(m.group("id"))
            self.command = m.group("command")

            args = m.group("args")
            args = args.split(",")

            for a in args:
                if len(a) > 0:
                    a = a.rstrip(',')
                    self.args.append(a)


class response(network_object):

    def __init__(self, data, r_id):
        network_object.__init__(self, data)
        self.request_id = r_id
        self.fields = []

