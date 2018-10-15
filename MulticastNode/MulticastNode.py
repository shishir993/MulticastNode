
from datetime import datetime
import socket
import struct

MCAST_GRP = '224.0.0.250'
MCAST_PORT = 7680
IS_ALL_GROUPS = True

def receive():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if IS_ALL_GROUPS:
        # on this port, receives ALL multicast groups
        sock.bind(('', MCAST_PORT))
    else:
        # on this port, listen ONLY to MCAST_GRP
        sock.bind((MCAST_GRP, MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        print("Waiting for packet")
        print(sock.recv(1024))

def send():
    # regarding socket.IP_MULTICAST_TTL
    # ---------------------------------
    # for all packets sent, after two hops on the network the packet will not 
    # be re-sent/broadcast (see https://www.tldp.org/HOWTO/Multicast-HOWTO-6.html)
    MULTICAST_TTL = 0

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
    msg = "join_" + str(datetime.now())
    print("Sending: < " + msg + " >")
    sock.sendto(str.encode(msg), (MCAST_GRP, MCAST_PORT))

if __name__ == "__main__":
    op = input("send or recv? ")
    if op == "send":
        send()
    elif op == "recv":
        receive()
    else:
        print("Unsupported command")
