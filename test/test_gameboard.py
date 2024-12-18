import pytest
import Main as main

@pytest.fixture
def ttt_board():
    return main.tictactoe()


def test_board_init(ttt_board):
    board = ttt_board.get_board()

    assert len(board) == 3, f"board length is not {3}"
    assert all(len(row) == 3 for row in board), f"row lengths are not {3}"
    assert all(cell == "" for row in board for cell in row), f"not all cells are '' "



def test_set_valid_moves(ttt_board):
    ttt_board.set_move_on_board(["0", "1"], "X")
    ttt_board.set_move_on_board(["1", "2"], 5)
    ttt_board.set_move_on_board(["2", "0"], True)
    board = ttt_board.get_board()

    assert board[0][1] == "X", f"board not showing a move in the specific location"
    assert board[1][2] == 5, f"board not showing a move in the specific location"
    assert board[2][0] == True, f"board not showing a move in the specific location"

def test_set_invalid_moves(ttt_board):
    with pytest.raises(IndexError):
        ttt_board.set_move_on_board(["3", "1"], "X")

    with pytest.raises(IndexError):
        ttt_board.set_move_on_board(["2", "4"], "X")