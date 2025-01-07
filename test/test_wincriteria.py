import pytest

## Double import. You're importing "Main" and then "PatternResult"
## prefer from ___ import things, you're, using, only
## If you're using a bunch, then I'd recommend: 
## import Main as var 
## Then use contents as "var.thing"
import Main
from Main import PatternResult
from unittest.mock import Mock, patch


## Your fixtures aren't scoped. This may not be a problem 
## But I'd recommend always scoping them
@pytest.fixture
def mock_get_board():
    return Mock()

###
### Ok, so I don't know much about how mock/patch work in python
### But I'm not sure this needs to be a fixture? Uncertain. 
###
### Edit: The way you're testing this it works but it's a bit clunky 
### The fact that there's 1 Main instance with mock_get_board is a little 
### 
###
@pytest.fixture
def wincriteria(mock_get_board):
    mock_get_board.return_value = [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""]
    ]
    return Main.tttwin(getboard=mock_get_board, winlength=3)



## This is the correct way to use patch, and it works just fine. The 
## alternative I'd recommend is to create a pattern_checker class 
## that you'd be able to pass in. If you did something like that, then 
## You'd be able to mock the class rather than need to patch the object. 
## They're functionally (as far as unit tests go) the same, but could have 
## usability differences depending on how you're testing/what you're doing 
## with the object. 
def test_game_won(wincriteria):
    with patch.object(wincriteria, "check_pattern", return_value=(True, "X")):
        result = wincriteria.game_is_won()

    assert result, f"Game is NOT over but it should be"


def test_game_not_won(wincriteria):
    with patch.object(wincriteria, "check_pattern", return_value=(False, None)):
        result = wincriteria.game_is_won()

    assert None == result, f"Game is over but it should NOT be"


# This test doesn't do much because I end the for loop immediately and then it returns. Not sure how to test this method/ if I need to..?
### This test is awkward because: 
### 1) You're setting `mock_get_board.return_value` in the test but then, you're immediately bailing. 
###    The entirity of the test comes down to "search_board"'s return, not the actual contents of the board.
### 2) You lack the required "completeness" in the test to know if this provides value. 
###
### This is one of the cases where I think mock/patch is a good use but it's more complicated than just a simple return. 
### If you used mock/patch to substitute search_board with a method you have more control over, you could do something like
### "Return true after X calls" so you know it's actually checking the WHOLE board.
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
### This test is an extension of the issues I have above, but is a better test by far. 
### This is, maybe intentionally I'm not sure, allowing the check_pattern code to loop 
### Over all the board, seeing 'search_board' return false every time 
### and leading to a cats game
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
### Think it's really really cool that you realized, probably through the test
### that the method doesn't actually do what you think it does. 
### 
### This is one of the power of tests! 
def test_tie_game(mock_get_board, wincriteria):
    mock_get_board.return_value = [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"]
    ]
    assert wincriteria.game_is_tie(), f"Game is not a tie"
