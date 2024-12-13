import pytest
import Main as main

parameters1 = [(['1', '0'], True), (['3', '1'], False), (['g', '1'], False), (['1', 'd'], False)]



@pytest.mark.parametrize('test_inputs, expected_output', parameters1)
def test_valid_inputs(test_inputs, expected_output):
    rules = main.tttinputrules(["0", "1", "2"])

    assert rules.valid_inputs(test_inputs) == expected_output


parameters2 = [([['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0']], ['0','0'], False), ([[0, 0, 0], [0, 0, 0], [0, 0, ""]], ['2','2'], True)]


@pytest.mark.parametrize('test_board, test_inputs, expected_output', parameters2)
def test_spot_is_playable(test_board,test_inputs, expected_output):
    rules = main.tttinputrules(["0", "1", "2"])
    assert rules.spot_is_playable(test_board,test_inputs) == expected_output
