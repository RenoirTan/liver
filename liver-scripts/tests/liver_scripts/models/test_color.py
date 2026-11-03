import pytest
from liver_scripts.models.color import validate_hex_color


@pytest.mark.parametrize(
    "input,expected,throw",
    [
        ("#123456", True, True),
        ("#abcdef", True, True),
        ("#ABC", True, True),
        ("#12abcdef", True, True),
        ("#1234", True, True),
        ("#Ab3202", True, True),

        ("#bad ", False, True),
        ("#12345", False, True),
        ("#Oops", False, True),
        ("abc", False, True),
        (" #abc", False, True),
    ]
)
def test_validate_hex_color(input: str, expected: bool, throw: bool):
    if throw and not expected:
        with pytest.raises(ValueError):
            validate_hex_color(input, throw=True)
    else:
        assert validate_hex_color(input, throw=throw) == expected
