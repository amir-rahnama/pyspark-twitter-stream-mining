# -*- coding: utf-8 -*-

import socket
import sys
import select   

def broadcast_data (sock, message):
    for socket in connection_list:
        if socket != socket_server and socket != sock :
            try :
                socket.send(message)
            except :
                socket.close()
                connection_list.remove(socket)

if __name__ == "__main__":
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 9999)
    connection_list = []
    print >>sys.stderr, 'starting up on %s port %s' % server_address

    socket_server.bind(server_address)
    socket_server.listen(10)
    connection_list.append(socket_server)

    while True:
        read_sockets,write_sockets,error_sockets = select.select(connection_list,[],[])
        
        # new connection
        for sock in read_sockets:
            if sock == socket_server:
                sockfd, addr = socket_server.accept()
                connection_list.append(sockfd)
                print "Client (%s, %s) connected" % addr
                
            else: 
                try:
                    data = sock.recv(4096).decode('utf-8')
                    
                    if data:
                        broadcast_data(sockfd, data)
                except:
                    sock.close()
                    connection_list.remove(sock)
                    continue

    sock.close()
