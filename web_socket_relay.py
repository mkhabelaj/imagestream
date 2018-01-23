import sys
import threading
import tornado
from tornado.ioloop import IOLoop
from web_socket_server import WSHandler, clients
from socket_server import SocketServer

PORT = int(sys.argv[1])
WEB_STREAM_PORT = int(sys.argv[2])
STREAM_SECRET = sys.argv[3]

if not PORT:
    print('No port provided, exiting....')
    sys.exit()

if not WEB_STREAM_PORT:
    print('No web stream port provided, exiting....')
    sys.exit()

if not STREAM_SECRET:
    print('No web stream secret provided, exiting....')
    sys.exit()

sock_server = SocketServer(port=PORT)

print("Web stream information web stream port:{wsp}, socket stream port{port}".format(
    wsp=WEB_STREAM_PORT,
    port=PORT
))


def stream():
    print("Beginning image stream")
    image_generator = sock_server.initiate_server()
    while True:
        data = next(image_generator)
        if data:
            try:
                [client.write_message(data, binary=True) for client in clients]
            except Exception as ex:
                print(ex)


def main():
    t = threading.Thread(target=stream, args=())
    t.setDaemon(True)
    t.start()
    app = tornado.web.Application([(r"/{secret}".format(secret=STREAM_SECRET), WSHandler), ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(WEB_STREAM_PORT)
    print('Starting web server')
    IOLoop.instance().start()


if __name__ == "__main__":
    main()
