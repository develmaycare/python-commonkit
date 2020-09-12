from commonkit.exceptions import *
import pytest


class TestIMustBeMissingSomething(object):

    def test_init(self):
        with pytest.raises(IMustBeMissingSomething):
            raise IMustBeMissingSomething(self.__class__.__name__, "testing")
