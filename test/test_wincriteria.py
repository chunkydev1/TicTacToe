import pytest
import Main
from Main import PatternResult
from unittest.mock import Mock, patch


@pytest.fixture
def mock_get_board():
    return Mock()


@pytest.fixture
def wincriteria(mock_get_board):
    mock_get_board.return_value = [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""]
    ]
    return Main.tttwin(getboard=mock_get_board, winlength=3)


def test_game_won(wincriteria):
    with patch.object(wincriteria, "check_pattern", return_value=(True, "X")):
        result = wincriteria.game_is_won()

    assert result, f"Game is NOT over but it should be"


def test_game_not_won(wincriteria):
    with patch.object(wincriteria, "check_pattern", return_value=(False, None)):
        result = wincriteria.game_is_won()

    assert None == result, f"Game is over but it should NOT be"


# This test doesn't do much because I end the for loop immediately and then it returns. Not sure how to test this method/ if I need to..?
def test_check_pattern_win(mock_get_board, wincriteria):
    mock_get_board.return_value = [
        ["X", "", ""],
        ["", "", ""],
        ["", "", ""]
    ]
    with patch.object(wincriteria, "search_board", return_value=True):
        result = wincriteria.check_pattern()

    assert result == PatternResult(True, "X"), f"failed for some reason"


# This test doesn't do much because I end the for loop immediately and then it returns. Not sure how to test this method/ if I need to..?
def test_check_pattern_no_win(mock_get_board, wincriteria):
    mock_get_board.return_value = [
        ["X", "", ""],
        ["", "", ""],
        ["", "", ""]
    ]

    with patch.object(wincriteria, "search_board", return_value=False):
        result = wincriteria.check_pattern()

    assert result == PatternResult(False, None), f'failed for another reason'


def test_search_board_win(mock_get_board, wincriteria):
    mock_get_board.return_value = [
        ["X", "X", "X"],
        ["X", "X", "X"],
        ["X", "X", "X"]
    ]
    assert wincriteria.search_board(0, 0, 0, 1, 3, "X"), f"Search_board did NOT find a HORIZONTAL win on the top row"
    assert wincriteria.search_board(1, 0, 0, 1, 3, "X"), f"Search_board did NOT find a HORIZONTAL win on the middle row"
    assert wincriteria.search_board(2, 0, 0, 1, 3, "X"), f"Search_board did NOT find a HORIZONTAL win on the bottom row"

    assert wincriteria.search_board(0, 0, 1, 0, 3, "X"), f"Search_board did NOT find a VERTICAL win in the left column"
    assert wincriteria.search_board(0, 1, 1, 0, 3,
                                    "X"), f"Search_board did NOT find a VERTICAL win in the middle column"
    assert wincriteria.search_board(0, 2, 1, 0, 3, "X"), f"Search_board did NOT find a VERTICAL win in the right column"

    assert wincriteria.search_board(0, 0, 1, 1, 3, "X"), f"Search_board did NOT find a DIAGONAL (Left to right) win"
    assert wincriteria.search_board(0, 2, 1, -1, 3, "X"), f"Search_board did NOT find a DIAGONAL (right to left) win"


def test_search_board_no_win(mock_get_board, wincriteria):
    mock_get_board.return_value = [
        ["X", "X", "0"],
        ["X", "X", "X"],
        ["0", "X", "0"]
    ]
    assert False == wincriteria.search_board(0, 0, 0, 1, 3,
                                             "X"), f"search_board did find a win HORIZONTAL win on the top row"
    assert False == wincriteria.search_board(0, 0, 1, 0, 3,
                                             "X"), f"search_board did find a win VERTICAL win in the first column"
    assert False == wincriteria.search_board(0, 0, 1, 1, 3,
                                             "X"), f"search_board did find a win DIAGONAL win (left to right)"


# Realized it only looks for a full board, not actually for a tie.
def test_tie_game(mock_get_board, wincriteria):
    mock_get_board.return_value = [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"]
    ]
    assert wincriteria.game_is_tie(), f"Game is not a tie"
