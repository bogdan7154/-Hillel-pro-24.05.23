import unittest.mock as mock
from Unit_tests_dz.drunk_polish_calculator import op_plus, op_minus, op_divide, op_multiply, main


def test_op_plus():
    assert op_plus(2, 3) == 5
    assert op_plus(-5, 10) == 5
    assert op_plus(0, 0) == 0


def test_op_minus():
    assert op_minus(5, 2) == -3
    assert op_minus(10, -5) == -15
    assert op_minus(0, 0) == 0


def test_op_multiply():
    assert op_multiply(2, 3) == 6
    assert op_multiply(-5, 10) == -50
    assert op_multiply(0, 5) == 0


def test_op_divide():
    assert op_divide(10, 2) == 5
    assert op_divide(-20, 4) == -5
    assert op_divide(0, 5) == 0

'''''
def test_main(capsys):
    with pytest.raises(SystemExit) as e:
        input_string = '5 3 + 2 *'
        with mock.patch('builtins.input', return_value=input_string):
            main()

    assert e.type == SystemExit
    assert str(e.value) == '0'

    captured = capsys.readouterr()
    assert captured.out.strip() == '16.0'



def test_main(capsys):
    with pytest.raises(SystemExit) as e:
        input_string = '5 3 + 2 *'
        with mock.patch('builtins.input', return_value=input_string):
            with mock.patch('sys.stdout', new=mock.MagicMock()) as mock_stdout:
                main()
                captured = mock_stdout.getvalue().strip()

    assert e.type == SystemExit
    assert str(e.value) == '0'
    assert captured == '16.0'
'''''

def test_main(capsys):
    input_string = '5 3 + 2 *'
    with mock.patch('builtins.input', return_value=input_string), \
         mock.patch('sys.stdout', new=mock.MagicMock()) as mock_stdout, \
         mock.patch('sys.exit') as mock_exit:

        main()

        captured = mock_stdout.getvalue().strip()
        mock_exit.assert_called_once_with(0)
        assert captured == '16.0'
