import threading

import tornado
from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler
import cv2 as cv

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

class Camera():
    def __init__(self):
        self.capture = cv.VideoCapture(0)

    def takeImage(self):
        # img = self.capture
        ret, frame = self.capture.read()
        # img = cv.imread(frame)
        img = cv.imencode(".jpg", frame)[1].tostring()
        # type(img)
        return img
        # return frame

camera = Camera()

def testinfy():
    count = 0
    while True:
        img = camera.takeImage()
        # print('called')
        try:
            # print('valid')
            # [client.write_message("{count}".format(count=count)) for client in clients]
            [client.write_message(img,binary=True) for client in clients]
        except Exception as ex:
            # print('valid')
            print(ex)
        count += 1


def main():
    t = threading.Thread(target=testinfy, args=())
    t.setDaemon(True)
    t.start()
    app = tornado.web.Application([
        (r"/camera", WSHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8090)
    IOLoop.instance().start()

if __name__ == "__main__":
    main()