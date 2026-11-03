import pytest
from liver_scripts.models.style import (
    PartialStyle,
    Style,
    ResolvedStyle
)
from liver_scripts.models.text_style import TextStyle


@pytest.mark.parametrize(
    "input,color,opacity,bold,italic,underline",
    [
        ("#abcdef/7f/biu", "#abcdef", 0x7F, True, True, True),
        ("#123456//b", "#123456", 0xFF, True, False, False),
    ]
)
def test_parse_style(
    input: str,
    color: str,
    opacity: int,
    bold: bool,
    italic: bool,
    underline: bool,
):
    expected_text_style = TextStyle(bold=bold, italic=italic, underline=underline)
    expected_style = Style(color=color, opacity=opacity, text_style=expected_text_style)
    style = PartialStyle.parse(input).to_full()
    assert style == expected_style
