from commonkit.versions import STAGE, Compare, Version


class TestCompare(object):

    def test_is_equal_to(self):
        c = Compare("1.1.0", "1.1.0")
        assert c.is_equal_to is True

    def test_is_greater_than(self):
        c = Compare("1.0.0", "0.9.0")
        assert c.is_greater_than is True

    def test_is_less_than(self):
        c = Compare("1.9.9", "2.0.0")
        assert c.is_less_than is True


class TestVersion(object):

    def test_build(self):
        v = Version("1.0.0-d")
        assert v.build is None

        v = Version("1.0.0-d+testing")
        assert v.build == "testing"

    def test_bump(self):
        v = Version("0.1.1-d")
        assert v.bump(major=True).identifier == "1.0.0-d"

        v = Version("0.1.1-d")
        assert v.bump(minor=True).identifier == "0.2.0-d"

        v = Version("0.1.1-d")
        assert v.bump(patch=True).identifier == "0.1.2-d"

        v = Version("0.1.1-d")
        assert v.bump(build="testing").identifier == "0.1.1-d+testing"

        v = Version("0.1.1-d")
        assert v.bump(status="b").identifier == "0.1.1-b"

        v = Version("0.1.1-d")
        assert v.bump(major=True, status="").identifier == "1.0.0"

    def test_get_stage(self):
        v = Version("1.0.0")
        assert v.get_stage() == STAGE.LIVE

        v = Version("1.0.0-b")
        assert v.get_stage() == STAGE.BETA

        v = Version("1.0.0-z")
        assert v.get_stage() == "unknown"

    def test_major(self):
        v = Version("3.0.0")
        assert v.major == 3

    def test_minor(self):
        v = Version("3.2.0")
        assert v.minor == 2

    def test_patch(self):
        v = Version("3.2.5")
        assert v.patch == 5

    def test_pep440(self):
        v = Version("0.1.0-d")
        assert v.pep440 == "0.1.0"

    def test_status(self):
        v = Version("1.1.0")
        assert v.status is None

        v = Version("1.1.0-r")
        assert v.status == "r"

    def test_str(self):
        v = Version("3.2.0")
        assert str(v) == "3.2.0"
