from socket import *
from kalah_packets import *


class SocketError(Exception):
    pass

def sock_recvall(sock: socket, size: int) -> bytearray:
    data = bytearray()
    while len(data) < size:
        recv_bytes = sock.recv(size)
        if len(recv_bytes) == 0:
            raise SocketError
        data.extend(recv_bytes)
    return data


def sock_recv_packet(sock: socket) -> KalahPacket:
    packet_len_bytes = sock_recvall(sock, 2)
    packet_len = int.from_bytes(packet_len_bytes, byteorder='big')
    packet_bytes = sock_recvall(sock, packet_len)
    return packet_deserialize(packet_bytes)

def sock_send_packet(sock: socket, packet: KalahPacket):
    msg = bytearray()
    packet_bytes = packet_serialize(packet)
    packet_len = len(packet_bytes)
    msg.extend(packet_len.to_bytes(byteorder='big', length=2))
    msg.extend(packet_bytes)
    sock.sendall(msg)