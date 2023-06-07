import pytest
from Unit_tests_dz.drunk_polish_calculator import op_plus, op_minus, op_divide, op_multiply, main


def test_op_plus():
    assert op_plus(2, 3) == 5
    assert op_plus(-5, 10) == 5
    assert op_plus(0, 0) == 0


def test_op_minus():
    assert op_minus(5, 2) == 3
    assert op_minus(10, -5) == 15
    assert op_minus(0, 0) == 0


def test_op_multiply():
    assert op_multiply(2, 3) == 6
    assert op_multiply(-5, 10) == -50
    assert op_multiply(0, 5) == 0


def test_op_divide():
    assert op_divide(10, 2) == 5
    assert op_divide(-20, 4) == -5
    assert op_divide(0, 5) == 0
    with pytest.raises(ZeroDivisionError):
        op_divide(10, 0)  # Проверка деления на ноль


def test_main(capsys, monkeypatch):
    input_str = "5 3 + 2 *"
    input_mock = lambda _: input_str
    output_mock = lambda x: None

    monkeypatch.setattr('builtins.input', input_mock)
    monkeypatch.setattr('builtins.print', output_mock)

    main()

    captured = capsys.readouterr()
    assert captured.out.strip() == '16.0\n'
