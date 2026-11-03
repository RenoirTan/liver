import pytest
from liver_scripts.models.text_style import TextStyle


@pytest.mark.parametrize(
    "input,reference",
    [
        ("", TextStyle(bold=False, italic=False, underline=False)),
        ("b", TextStyle(bold=True, italic=False, underline=False)),
        ("i", TextStyle(bold=False, italic=True, underline=False)),
        ("u", TextStyle(bold=False, italic=False, underline=True)),
        ("bi", TextStyle(bold=True, italic=True, underline=False)),
        ("bu", TextStyle(bold=True, italic=False, underline=True)),
        ("iu", TextStyle(bold=False, italic=True, underline=True)),
        ("biu", TextStyle(bold=True, italic=True, underline=True)),
    ]
)
def test_text_style(input: str, reference: TextStyle):
    text_style = TextStyle.parse(input)
    assert text_style == reference
