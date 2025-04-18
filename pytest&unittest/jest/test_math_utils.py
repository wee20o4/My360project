from math_utils import add, subtract

def test_add():
    assert add(2, 3) == 5, "2 + 3 should equal 5"
    assert add(-1, 1) == 0, "-1 + 1 should equal 0"
    assert add(0, 0) == 0, "0 + 0 should equal 0"

def test_subtract():
    assert subtract(5, 3) == 2, "5 - 3 should equal 2"
    assert subtract(3, 5) == -2, "3 - 5 should equal -2"
    assert subtract(0, 0) == 0, "0 - 0 should equal 0"