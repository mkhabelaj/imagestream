import select
import socket
from struct import unpack


class SocketServer:

    def __init__(self,
                 number_of_listeners=10,
                 size_byte_length=8,
                 recv_buffer=4096,
                 port=5000,
                 address='0.0.0.0'
                 ):
        print('setting up socket server. address: {address}, port: {port}'.format(address=address,port=port))
        self.connection_list = []  # list of client connections
        self.recv_buffer = recv_buffer  # keep it as an exponent of 2
        self.port = port
        self.size_byte_length = size_byte_length

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((address, self.port))
        self.server_socket.listen(number_of_listeners)

        # add socket to client list
        self.connection_list.append(self.server_socket)

    def initiate_server(self):
        print("initiating stream server")

        while 1:
            # Get the list of sockets that are ready to be read from
            read_sockets, write_sockets, error_sockets = select.select(self.connection_list, [], [])
            for sock in read_sockets:
                '''
                Check if if the server socket is equal to sock,
                and if it is equal to sock except the new connection
                '''
                if sock == self.server_socket:
                    sockfd, addr = self.server_socket.accept()
                    self.connection_list.append(sockfd)
                    print("Client (%s, %s) connected" % addr)
                else:
                    try:
                        bs = sock.recv(self.size_byte_length)
                        data = b''
                        if bs:
                            (length,) = unpack('>Q', bs)
                            while len(data) < length:
                                to_read = length - len(data)
                                data += sock.recv(4096 if to_read > 4096 else to_read)
                            yield data
                    except Exception as ex:
                        print(ex)
                        print("Client (%s, %s) is offline" % addr)
                        sock.close()
                        self.connection_list.remove(sock)
                        continue

    def str_to_bytes(self, str_to_convert):
        return str.encode(str_to_convert, 'UTF-8')

    def bytes_to_str(self, data_to_convert):
        return str(data_to_convert, 'utf-8')


