import pytest
import Main as main

parameters1 = [(['1', '0'], True), (['3', '1'], False), (['g', '1'], False), (['1', 'd'], False)]


### 
### I HATE the "expected inputs expected outputs" pattern 
### test_valid_inputs and test_invalid_inputs
### Only pass in the inputs, outputs should be known by the tests. 
###
@pytest.mark.parametrize('test_inputs, expected_output', parameters1)
def test_valid_inputs(test_inputs, expected_output):
    rules = main.tttinputrules(["0", "1", "2"])

    ### No assert messages
    assert rules.valid_inputs(test_inputs) == expected_output


### If you're ever starting an object definition as "[([[" maybe reconsider 
parameters2 = [(, ['0','0'], False), ([[0, 0, 0], [0, 0, 0], [0, 0, ""]], ['2','2'], True)]

@pytest.mark.parametrize('test_board, test_inputs, expected_output', parameters2)
def test_spot_is_playable(test_board,test_inputs, expected_output):
    rules = main.tttinputrules(["0", "1", "2"])

    ### No assert messages
    assert rules.spot_is_playable(test_board,test_inputs) == expected_output


def partial_board(empty_spots): 
	## empty spots is a list of (x, y, val)
	_board = [['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0']]
	for col, row, val in empty_spots: 
		_board[col][row] = val
	return _board

def full_board(): 
	return partial_board([])

def empty_board(): return [['', '', ''], ['', '', ''], ['', '', '']]


def get_spot_list(): 
	spots = []
	b = empty_board()
	for row, _ in enumerate(b): 
		for col, _ in enumerate(b[row]): 
			spots.append([str(col), str(row)])
	return spots 

@pytest.fixture(scope='function')
def rulefx(): 
	return main.tttinputrules(["0", "1", "2"])

@pytest.mark.parametrize(get_spot_list())
def test_empty_board_spot_playable(rulefx, spot): 
    assert rulefx.spot_is_playable(empty_board(), spot), 'empty board spot not playable'

@pytest.mark.parametrize(get_spot_list())
def test_full_board_not_playable(rulefx, spot): 
    assert not rulefx.spot_is_playable(full_board(), spot), 'full board spot playable'

@pytest.mark.parametrize(get_spot_list())
def test_partial_board_playable(rulefx, spot): 
	empty = [spot[0], spot[1], '']
    assert rulefx.spot_is_playable(partial_board(empty), spot), 'partial board spot not playable'


### The following is overkill, but I'm doing an example so here we go
def reversed_spot_list(): 
	l = get_spot_list()
	l.reverse()
	return l

def drop_middle(get_fx): 
	## Magic math here because the function just "knows" that the 
	## middle of the list is entry 5. 
	## I think a better way would be to do something like: 
	## length = len(get_fx)
	## bump = 0 if length % 2 == 0 else 1
	## low_lim = floor(length / 2 )
	## high_lim = floor(length / 2 ) + bump 
	## get_fx()[:low_lim] + get_fx()[high_lim:]
	return get_fx()[:4] + get_fx()[5:]

@pytest.mark.parametrize('play_spot', 'empty_spot'
	list(zip(
		## We drop the middle because we know it's 9 entries and a reversed list 
		## will match on the 5th item if you invert it. 
		drop_middle(get_spot_list), drop_middle(reversed_spot_list())
	)))
def test_partial_board_not_playable(rulefx, play_spot, empty_spot): 
	empty = [empty_spot[0], empty_spot[1], '']
	assert not rulefx.spot_is_playable(partial_board(empty), play_spot)


