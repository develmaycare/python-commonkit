from commonkit.context_managers import captured_output
from commonkit.shell.prompts import *


class TestingForm(Form):
    input1 = String("input1")
    input2 = String("input2")
    input3 = String("input3")


# Tests


def test_get_choice(monkeypatch):
    # Without choices.

    def mock_input1(label):
        return "1"

    monkeypatch.setattr("builtins.input", mock_input1)
    with captured_output() as (output, error):
        result = get_choice("Yes or No")
        assert "yes" == result

    # With choices.

    def mock_input3(label):
        return "3"

    choices = ["a", "b", "c"]
    monkeypatch.setattr("builtins.input", mock_input3)
    with captured_output() as (output, error):
        result = get_choice("Pick a Letter", choices=choices)
        assert "c" == result

    # With default.
    def mock_input_empty(label):
        return ""

    choices = ["a", "b", "c"]
    monkeypatch.setattr("builtins.input", mock_input_empty)
    with captured_output() as (output, error):
        result = get_choice("Pick a Letter", choices=choices, default="b")
        assert "b" == result

    # With invalid choice.
    def mock_input4(label):
        return "4"

    try:
        choices = ["a", "b", "c"]
        monkeypatch.setattr("builtins.input", mock_input4)
        with captured_output() as (output, error):
            get_choice("Pick a Letter", choices=choices, default="b")
            # self.assertTrue("Invalid" in output.getstring())
    except RecursionError:
        pass


def test_get_input(monkeypatch):
    # Without default value.
    def mock_input_testing(label):
        return "testing"

    monkeypatch.setattr("builtins.input", mock_input_testing)
    with captured_output() as (output, error):
        result = get_input("What Is This?")
        assert "testing" == result

    # With default value.
    def mock_input_empty(label):
        return ""

    monkeypatch.setattr("builtins.input", mock_input_empty)
    with captured_output() as (output, error):
        result = get_input("What Is This", default="testing")
        assert "testing" == result


class TestForm(object):

    def test_default(self, monkeypatch):
        def mock_input(label):
            return "testing"

        form = TestingForm()
        form.fields['input2'].default = "$input1"

        monkeypatch.setattr("builtins.input", mock_input)
        with captured_output() as (output, error):
            form.prompt()
            assert len(form.values) == 3

    def test_get(self):
        form = TestingForm()
        value = form.get("input1", default="testing")
        assert "testing" == value

    def test_get_fields(self):
        form = TestingForm()

        assert len(form.get_fields()) == 3

    def test_prompt(self, monkeypatch):
        def mock_input(label):
            return "testing"

        form = TestingForm()

        monkeypatch.setattr("builtins.input", mock_input)
        with captured_output() as (output, error):
            form.prompt()
            assert len(form.values) == 3


class TestInput(object):

    def test_get_type(self):
        i = Input("testing")
        assert str == i.get_type()

    def test_is_valid(self):
        i = Input("testing")
        assert i.is_valid() is True

        i = Input("Testing", required=True)
        assert i.is_valid() is False
        assert "Testing is required." == i.error

    def test_prompt(self, monkeypatch):
        i = Input("testing")

        def mock_input_yes(label):
            return "yes"

        monkeypatch.setattr("builtins.input", mock_input_yes)
        with captured_output() as (output, error):
            result = i.prompt()
            assert "yes" == result

        def mock_input3(label):
            return "3"

        choices = ["a", "b", "c"]
        i = Input("Pick a Letter", choices=choices, required=True)
        monkeypatch.setattr("builtins.input", mock_input3)
        with captured_output() as (output, error):
            result = i.prompt()
            assert "c" == result

        def mock_input_empty(label):
            return ""

        try:
            i = Input("testing", required=True)
            monkeypatch.setattr("builtins.input", mock_input_empty)
            with captured_output() as (output, error):
                i.prompt()
                # self.assertTrue("required" in output.getstring())
        except RecursionError:
            pass

    def test_repr(self):
        i = Input("testing")
        assert "<Input testing>" == repr(i)


class TestBoolean(object):

    def test_get_type(self):
        i = Boolean("testing")
        assert bool == i.get_type()

    def test_is_valid(self):
        i = Boolean("testing", required=True)
        assert i.is_valid() is False

        i.value = "not-a-boolean"
        assert i.is_valid() is False

        i.value = "no"
        assert i.is_valid() is True

        i.value = "yes"
        assert i.is_valid() is True
        assert i.to_python() is True


class TestDivider(object):

    def test_prompt(self):
        i = Divider(label="Testing")
        with captured_output() as (output, error):
            i.prompt()

            assert "Testing" in output.getvalue()
            assert "===" in output.getvalue()


class TestEmail(object):

    def test_is_valid(self):
        i = Email("testing", required=True)
        assert i.is_valid() is False

        i.value = "invalidemail.com"
        assert i.is_valid() is False

        i.value = "example@example.com"
        assert i.is_valid() is True


class TestFloat(object):

    def test_get_type(self):
        i = Float("testing")
        assert float == i.get_type()

    def test_is_valid(self):
        i = Float("testing", required=True)
        assert i.is_valid() is False

        i.value = "not-a-float"
        assert i.is_valid() is False

        i.value = "1.2345"
        assert i.is_valid() is True

        i.value = 1.2345
        assert i.is_valid() is True


class TestInteger(object):

    def test_get_type(self):
        i = Integer("testing")
        assert int == i.get_type()

    def test_is_valid(self):
        i = Integer("testing", required=True)
        assert i.is_valid() is False

        i.value = "not-an-integer"
        assert i.is_valid() is False

        i.value = "1.2"
        assert i.is_valid() is False

        i.value = 1
        assert i.is_valid() is True


class TestRegex(object):

    def test_is_valid(self):
        pattern = r"[0-9]*"
        i = Regex("testing", pattern, required=True)
        assert i.is_valid() is False

        i.value = "this doesn't match"
        assert i.is_valid() is False

        i.value = "1234"
        assert i.is_valid() is True

    def test_to_python(self):
        pattern = r"[0-9]*"
        i = Regex("testing", pattern, required=True)
        i.value = "this doesn't match"
        assert i.to_python() is None


class TestSecret(object):

    def test_prompt(self, monkeypatch):
        i = Secret("password")

        def mock_raw_input(prompt, stream, input):
            return "secret"

        monkeypatch.setattr("getpass._raw_input", mock_raw_input)
        # with patch("getpass._raw_input", return_value="secret"):
        with captured_output() as (output, error):
            result = i.prompt()
            assert "secret" == result

        def mock_raw_input_empty(prompt, stream, input):
            return ""

        i.required = True
        try:
            monkeypatch.setattr("getpass._raw_input", mock_raw_input_empty)
            # with patch('getpass._raw_input', return_value=""):
            with captured_output() as (output, error):
                i.prompt()
        except RecursionError:
            pass


class TestString(object):

    def test_is_valid(self):
        i = String("testing", maximum=10, minimum=3)
        assert i.is_valid() is False

        # Too short.
        i.value = "12"
        assert i.is_valid() is False

        # Over length.
        i.value = "12345678910"
        assert i.is_valid() is False

        # Minimum length.
        i.value = "123"
        assert i.is_valid() is True

        # Inside length.
        i.value = "123456789"
        assert i.is_valid() is True
