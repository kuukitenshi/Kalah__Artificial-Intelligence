from kalah import *

# KALAH STATE
# pass_turn
# to_move
# prev_move
# state

# KALAH
# initial

KALAH_STATE_SIZE = 1 + 1 + 1 + 14 * 1

def kalah_state_serialize(state: KalahState) -> bytearray:
    state_bytes = bytearray()
    state_bytes.extend(state.pass_turn.to_bytes(byteorder='big'))
    state_bytes.extend(state.to_move.to_bytes(byteorder='big'))
    prev_move = -2
    if hasattr(state, 'prev_move'):
        prev_move = state.prev_move
    state_bytes.extend(prev_move.to_bytes(length=1, byteorder='big', signed=True))
    for p in state.state:
        state_bytes.extend(p.to_bytes(length=1, byteorder='big'))
    return state_bytes

def kalah_state_deserialize(state_bytes: bytearray) -> KalahState:
    state = KalahState()
    state.pass_turn = bool.from_bytes(state_bytes[0:1], byteorder='big')
    state.to_move = int.from_bytes(state_bytes[1:2], byteorder='big')
    prev_move = int.from_bytes(state_bytes[2:3], byteorder='big', signed=True)
    if prev_move != -2:
        state.prev_move = prev_move
    board_state = []
    for i in range(3, len(state_bytes)):
        board_state.append(int.from_bytes(state_bytes[i:i+1], byteorder='big'))
    state.state = board_state
    return state