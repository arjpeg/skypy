from skypy.src.utils import remove_color_codes


def test_remove_color_codes() -> None:
    assert remove_color_codes("") == ""
    assert remove_color_codes("Hello") == "Hello"
    assert remove_color_codes("Hello\u00A7") == "Hello"
    assert remove_color_codes("Hello\u00A7bWorld") == "HelloWorld"
    assert remove_color_codes("Hello\u00A74World\u00A7") == "HelloWorld"
