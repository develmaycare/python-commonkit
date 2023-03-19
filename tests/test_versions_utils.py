from commonkit.versions import bump_version, get_current_version


def test_bump_version():
    v = bump_version("2.1.0", major=True)
    assert v == "3.0.0"


def test_get_current_version():
    assert get_current_version(path="nonexistent.txt") == "0.1.0-p"

    # This reads VERSION.txt in the same directory where tests are executed.
    assert get_current_version() != "0.1.0-p"
