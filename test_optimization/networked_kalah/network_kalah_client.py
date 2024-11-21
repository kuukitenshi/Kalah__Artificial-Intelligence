from kalah_sockets import *
from kalah import *


def network_kalah_client_start(address, port, player, verbose=False):
    with socket(AF_INET, SOCK_STREAM) as sock:
        try:
            sock.connect((address, port))
        except ConnectionRefusedError:
            print('Failed to connect to server!')
            return
        player_info_packet = PlayerInfoPacket(player.nome)
        sock_send_packet(sock, player_info_packet)
        while True:
            try:
                packet = sock_recv_packet(sock)
            except SocketError:
                print('Server closed!')
                exit(0)
            except:
                exit(0)
            if packet.packet_id == KALAH_PACKET_SERVER_GAME_STATE:
                if verbose:
                    print('Received state:')
                    print(packet.state)
                move = player.fun(packet.game, packet.state)
                if verbose:
                    print('SENDING MOVE:')
                    print(move)
                move_packet = ClientMovePacket(move)
                sock_send_packet(sock, move_packet)
            elif packet.packet_id == KALAH_PACKET_SERVER_TOURNAMENT_RESULT:
                print('\n', '-'*15, '[ TOURNAMENT ENDED ]', '-'*15, sep='')
                if packet.winner == 1:
                    print('VICTORY!')
                elif packet.winner == 2:
                    print('TIE!')
                else:
                    print('DEFEAT!')
                print('Scores:', packet.scores)
            else:
                print('ERROR BAD PACKET RECEIVED!')