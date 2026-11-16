import pytest

from version import wheel_version


@pytest.mark.parametrize(
    ("tag", "revision", "expected"),
    [
        ("FS2026.3", 0, "2026.3.0.0"),
        ("FS2023.1.1", 0, "2023.1.1.0"),
        ("FS2025.4c", 0, "2025.4.3.0"),
        ("FS2025.4a", 2, "2025.4.1.2"),
        ("2027.1.0", 0, "2027.1.0.0"),
        ("2027.01.02", 1, "2027.1.2.1"),
    ],
)
def test_wheel_version(tag, revision, expected):
    assert wheel_version(tag, revision) == expected


@pytest.mark.parametrize(
    "tag",
    [
        "FS2023.1.1a",
        "FS2026",
        "FS2026.3C",
        "2027.1",
        "v2027.1.0",
        "2027.1.0.0",
        "main",
    ],
)
def test_refuses_tag(tag):
    with pytest.raises(ValueError, match=repr(tag)):
        wheel_version(tag, 0)


def test_refuses_negative_revision():
    with pytest.raises(ValueError, match="revision"):
        wheel_version("2027.1.0", -1)
