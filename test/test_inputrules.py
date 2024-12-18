import pytest
import Main as main

@pytest.fixture
def inputrules():
    return main.tttinputrules(inputs=["0","1","2"])

@pytest.fixture
def ttt_board():
    return main.tictactoe()


def test_valid_inputs(inputrules):
    assert inputrules.valid_inputs(['0','1']), f"invalid inputs"
    assert inputrules.valid_inputs(['1', '2']), f"invalid inputs"
    assert inputrules.valid_inputs(['2', '0']), f"invalid inputs"

def test_invalid_inputs(inputrules):
    assert False == inputrules.valid_inputs(['3','1']), f"valid inputs"
    assert False == inputrules.valid_inputs(['1', 6]), f"valid inputs"
    assert False == inputrules.valid_inputs(['2', 'f']), f"valid inputs"





def test_spot_playable(inputrules,empty_ttt_board):
    board = ttt_board.get_board()
    assert inputrules.spot_is_playable(board,["0","1"]), f"spot is NOT playable"
    assert inputrules.spot_is_playable(board, ["2", "1"]), f"spot is NOT playable"

def test_spot_NOT_playable(inputrules,empty_ttt_board):
    board = ttt_board.get_board()
    ttt_board.set_move_on_board(["0", "1"], "X")
    ttt_board.set_move_on_board(["2", "1"], "O")

    assert False == inputrules.spot_is_playable(board,["0","1"]), f"spot is playable"
    assert False == inputrules.spot_is_playable(board, ["2", "1"]), f"spot is playable"