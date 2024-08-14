import sys
import pytest
from subprocess import call

CHECK = ["pip", "check"]
COV = "coverage"
PYTEST = ["pytest", "-vv", "--color=yes", "--tb=long", __file__]
TEST = [COV, "run", "--source=stringcase", "-m", *PYTEST]
REPORT = [COV, "report", "--show-missing", "--skip-covered", "--fail-under=83"]


@pytest.mark.parametrize(
    ["good", "name", "raw", "expected"],
    [
        (True, "camelcase", "foo_bar_baz", "fooBarBaz"),
        (True, "camelcase", "FooBarBaz", "fooBarBaz"),
        (True, "capitalcase", "foo_bar_baz", "Foo_bar_baz"),
        (True, "capitalcase", "FooBarBaz", "FooBarBaz"),
        (True, "constcase", "foo_bar_baz", "FOO_BAR_BAZ"),
        (True, "lowercase", "foo_bar_baz", "foo_bar_baz"),
        (True, "lowercase", "FooBarBaz", "foobarbaz"),
        (True, "pascalcase", "foo_bar_baz", "FooBarBaz"),
        (True, "pascalcase", "FooBarBaz", "FooBarBaz"),
        (True, "pathcase", "foo_bar_baz", "foo/bar/baz"),
        (True, "sentencecase", "foo_bar_baz", "Foo bar baz"),
        (True, "sentencecase", "FooBarBaz", "Foo bar baz"),
        (True, "snakecase", "foo_bar_baz", "foo_bar_baz"),
        (True, "spinalcase", "foo_bar_baz", "foo-bar-baz"),
        (True, "titlecase", "foo_bar_baz", "Foo Bar Baz"),
        (True, "trimcase", "foo_bar_baz", "foo_bar_baz"),
        (True, "trimcase", "FooBarBaz", "FooBarBaz"),
        (True, "uppercase", "foo_bar_baz", "FOO_BAR_BAZ"),
        (True, "uppercase", "FooBarBaz", "FOOBARBAZ"),
        # these are documented upstream but don't give the described output
        (False, "alphanumcase", "_Foo., Bar", "FooBar"),
        (False, "alphanumcase", "Foo_123 Bar!", "Foo123Bar"),
        (False, "constcase", "FooBarBaz", "_FOO_BAR_BAZ"),
        (False, "pathcase", "FooBarBaz", "/foo/bar/baz"),
        (False, "snakecase", "FooBarBaz", "_foo_bar_baz"),
        (False, "spinalcase", "FooBarBaz", "-foo-bar-baz"),
        (False, "titlecase", "FooBarBaz", " Foo Bar Baz"),
    ],
)
def test_stringcase(good: bool, name: str, raw: str, expected: str) -> None:
    """
    Verify behavior from README.

    see https://github.com/okunishinishi/python-stringcase

    known fails have been commented out
    """

    import stringcase

    method = getattr(stringcase, name)
    observed = method(raw)

    assert (
        observed == expected if good else observed != expected
    ), f"""({good}, "{name}", "{raw}", "{expected}")"""


if __name__ == "__main__":
    sys.exit(call(CHECK) or call(TEST) or call(REPORT))
