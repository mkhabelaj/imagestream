from tornado.websocket import WebSocketHandler

clients = []


class WSHandler(WebSocketHandler):
    def check_origin(self, origin):
        return True

    def on_message(self, message):
        self.write_message(u"You said: " + message)
        print(message)

    def data_received(self, chunk):
        pass

    def open(self):
        print("connection opened")
        clients.append(self)
        print(len(clients))

    def on_close(self):
        print('closing connection')
        clients.remove(self)
        print(len(clients))
