from exonviz_web import maths


def test_addition() -> None:
    assert maths.addition(1, 2) == 3
