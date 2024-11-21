from kalah_serialization import *
from kalah import *
import json

class KalahPacket():

    def __init__(self, packet_id: int):
        self.packet_id = packet_id


class KalahPacketSerializer():
    
    def __init__(self, packet_id):
        self.packet_id = packet_id

    def serialize(packet: KalahPacket) -> bytearray:
        raise NotImplementedError

    def deserialize(bytes: bytearray) -> KalahPacket:
        raise NotImplementedError


KALAH_PACKET_CLIENT_PLAYERINFO = 1
KALAH_PACKET_CLIENT_MOVE = 2
KALAH_PACKET_SERVER_GAME_STATE = 3
KALAH_PACKET_SERVER_TOURNAMENT_RESULT = 4

class PlayerInfoPacket(KalahPacket):

    def __init__(self, player_name):
        super().__init__(KALAH_PACKET_CLIENT_PLAYERINFO)
        self.player_name = player_name

class PlayerInfoPacketSerializer(KalahPacketSerializer):

    def __init__(self):
        super().__init__(KALAH_PACKET_CLIENT_PLAYERINFO)

    def serialize(self, packet: PlayerInfoPacket) -> bytearray:
        data = bytearray()
        data.extend(bytes(packet.player_name, encoding='utf-8'))
        return data
    
    def deserialize(self, msg_bytes: bytearray) -> PlayerInfoPacket:
        return PlayerInfoPacket(msg_bytes.decode())
    

class ClientMovePacket(KalahPacket):

    def __init__(self, action: int):
        super().__init__(KALAH_PACKET_CLIENT_MOVE)
        self.action = action

class ClientMovePacketSerializer(KalahPacketSerializer):

    def __init__(self):
        super().__init__(KALAH_PACKET_CLIENT_PLAYERINFO)

    def serialize(self, packet: ClientMovePacket) -> bytearray:
        data = bytearray()
        data.extend(packet.action.to_bytes(byteorder='big', length=1, signed=True))
        return data
    
    def deserialize(self, msg_bytes: bytearray) -> ClientMovePacket:
        action = int.from_bytes(msg_bytes, byteorder='big', signed=True)
        return ClientMovePacket(action)
    

class ServerGameStatePacket(KalahPacket):

    def __init__(self, game, state):
        super().__init__(KALAH_PACKET_SERVER_GAME_STATE)
        self.game = game
        self.state = state

class ServerGameStatePacketSerializer(KalahPacketSerializer):

    def __init__(self):
        super().__init__(KALAH_PACKET_SERVER_GAME_STATE)

    def serialize(self, packet: ServerGameStatePacket) -> bytearray:
        data = bytearray()
        data.extend(kalah_state_serialize(packet.game.initial))
        data.extend(kalah_state_serialize(packet.state))
        return data
    
    def deserialize(self, msg_bytes: bytearray) -> ServerGameStatePacket:
        initial = kalah_state_deserialize(msg_bytes)
        state = kalah_state_deserialize(msg_bytes[KALAH_STATE_SIZE:])
        game = Kalah()
        game.initial = initial
        return ServerGameStatePacket(game, state)
    

class TournamentResultPacket(KalahPacket):

    # 0 - lost, 1 - win, 2- tie
    def __init__(self, winner: int, scores: dict):
        super().__init__(KALAH_PACKET_SERVER_TOURNAMENT_RESULT)
        self.winner = winner
        self.scores = scores

class TournamentResultPacketSerializer(KalahPacketSerializer):

    def __init__(self):
        super().__init__(KALAH_PACKET_SERVER_TOURNAMENT_RESULT)

    def serialize(self, packet: TournamentResultPacket) -> bytearray:
        data = bytearray()
        winner_bytes = packet.winner.to_bytes(length=1, byteorder='big')
        data.extend(winner_bytes)
        scores_str = json.dumps(packet.scores)
        data.extend(bytes(scores_str, encoding='utf-8'))
        return data
    
    def deserialize(self, msg_bytes: bytearray) -> TournamentResultPacket:
        winner = int.from_bytes(msg_bytes[0:1], byteorder='big')
        scores_str = msg_bytes[1:].decode()
        scores = json.loads(scores_str)
        return TournamentResultPacket(winner, scores)


_serializers = {
    KALAH_PACKET_CLIENT_PLAYERINFO: PlayerInfoPacketSerializer(),
    KALAH_PACKET_CLIENT_MOVE: ClientMovePacketSerializer(),
    KALAH_PACKET_SERVER_GAME_STATE: ServerGameStatePacketSerializer(),
    KALAH_PACKET_SERVER_TOURNAMENT_RESULT: TournamentResultPacketSerializer()
}


def packet_serialize(packet: KalahPacket) -> bytearray:
    packet_serialized = bytearray()
    packet_serialized.extend(packet.packet_id.to_bytes(length=1, byteorder='big'))
    packet_serialized.extend(_serializers[packet.packet_id].serialize(packet))
    return packet_serialized

def packet_deserialize(packet_bytes: bytearray) -> KalahPacket:
    packet_id = int.from_bytes(packet_bytes[0:1], byteorder='big')
    return _serializers[packet_id].deserialize(packet_bytes[1:])