import sys
import os
from torneio import *
from kalah_serialization import *
from kalah_sockets import *
from signal import *
from socket import *
from threading import *


connected_players = []
game_running_lock = Lock()
server_socket = None


class NetworkPlayer():

    def __init__(self, nome, sock):
        self.nome = nome
        self.sock: socket.socket = sock

    def display(self):
        print(self.nome+" ")

    def fun(self, game, state):
        game_state_packet = ServerGameStatePacket(game, state)
        try:
            sock_send_packet(self.sock, game_state_packet)
            move_packet = sock_recv_packet(self.sock)
        except SocketError:
            print(f'{self.nome} disconnected!')
            raise SocketError
        if move_packet.packet_id != KALAH_PACKET_CLIENT_MOVE:
            print('BAD PACKET RECEIVED MOVE!')
        return move_packet.action
    
    def send_tournament_result(self, packet: TournamentResultPacket):
        try:
            sock_send_packet(self.sock, packet)
        except SocketError:
            pass


def client_accept_thread():
    print('Waiting for players to connect...')
    while True:
        try:
            client_sock, _ = server_socket.accept()
        except:
            break
        if game_running_lock.locked():
            client_sock.close()
            continue
        player_info_packet = sock_recv_packet(client_sock)
        if player_info_packet.packet_id != KALAH_PACKET_CLIENT_PLAYERINFO:
            print('BAD PACKET RECEIVED!')
            client_sock.close()
            continue
        player_name = player_info_packet.player_name
        print(f'Player connected: {player_name}')
        player = NetworkPlayer(player_name, client_sock)
        connected_players.append(player)


def print_menu():
    print('COMMANDS:')
    print(' > help - help menu')
    print(' > start <rounds> [game id] - to start the tournament')
    print(' > playerlist - to check connected players')
    print(' > stop - terminate the server')


def start_tournament(rounds, game_id):
    game_running_lock.acquire()
    print(f'Started tournament with id {game_id} and number of rounds {rounds}')
    try:
        result = torneio(rounds, connected_players, game_id)
        best_score = max(x for x in result.values())
        is_tie = sum(1 for x in result.values() if x == best_score) > 1
        print('Tournament result:')
        print(result)
        for p in connected_players:
            packet = TournamentResultPacket(0, result)
            if result[p.nome] == best_score:
                packet.winner = 1 if not is_tie else 2
            p.send_tournament_result(packet)
    except:
        print('An error ocurred, tournament was aborted!')
    finally:
        game_running_lock.release()


def stop_server():
    server_socket.close()
    print('Server closed!')
    os._exit(0)


def user_input():
    full_input = input('> ').split(' ', maxsplit=2)
    command = full_input[0]
    args = []
    if len(full_input) > 1:
        args = full_input[1:]
    if command == 'playerlist':
        if len(connected_players) == 0:
            print('There are no players connected :(')
        else:
            print('PLAYERLIST:')
            for p in connected_players:
                print(f'> {p.nome}')
    elif command == 'start':
        if len(args) == 0:
            print('ERROR: Invalid arguments! Usage start <rounds> [game id]')
            return
        if len(connected_players) == 0:
            print('ERROR: You can\'t start the tournament with no players connected!')
            print('')
            return
        if len(connected_players) == 1:
            print('ERROR! You need more than 1 player to start a tournament')
            print('')
            return
        rounds = int(args[0])
        if rounds <= 0:
            print('ERROR: Invalid number of rounds!')
            print('')
            return
        game_id = 0
        if len(args) >= 2:
            game_id = int(args[1])
            if game_id < -1 or game_id > 256:
                print('ERROR: Invalid game id!')
                print('')
                return
        start_tournament(rounds, game_id)
    elif command == 'help':
        print_menu()
    elif command == 'stop':
        stop_server()
    else:
        print('(!) Invalid command! Run \'help\' to check the command list.')
    print('')


def signal_handler(signum, frame):
    if signum == SIGINT:
        print('')
        stop_server()
    

if __name__ == '__main__':
    signal(SIGINT, signal_handler)
    argc = len(sys.argv)
    if argc < 2:
        print(f'Usage {sys.argv[0]} <port>')
        exit(-1)
    port = int(sys.argv[1])
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen()
    print('Server started!')
    thread = Thread(target=client_accept_thread)
    thread.start()
    print_menu()
    print('')
    while True:
        try:
            user_input()
        except:
            break