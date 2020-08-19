from commonkit.context_managers import captured_output
from commonkit.shell.feedback import *


# Tests


def test_blue():
    with captured_output() as (output, error):
        blue("This is blue.")

        assert "This is blue." in output.getvalue()


def test_colorize():
    """Check output of colorize function."""
    output = colorize(RED, "This is a test", prefix="Testing:", suffix="<-- look")
    assert "This is a test" in output
    assert "Testing:" in output
    assert "<-- look" in output


def test_green():
    with captured_output() as (output, error):
        green("This is green.")
        assert "This is green." in output.getvalue()


def test_hr():
    with captured_output() as (output, error):
        hr(character="=", color=red, size=10)
        assert "===" in output.getvalue()

    with captured_output() as (output, error):
        hr(character="=", size=10)
        assert "===" in output.getvalue()


def test_plain():
    with captured_output() as (output, error):
        plain("This is plain.", prefix="Testing:", suffix="wow")
        assert "This is plain." in output.getvalue()


def test_red():
    with captured_output() as (output, error):
        red("This is red.")
        assert "This is red." in output.getvalue()


def test_yellow():
    with captured_output() as (output, error):
        yellow("This is yellow.")
        assert "This is yellow." in output.getvalue()


class TestFeedback(object):

    def test_cr(self):
        feedback = Feedback()
        feedback.plain("This is a message.")
        feedback.cr()
        assert len(feedback.messages) == 2

    def test_feedback(self):
        """Check standard feedback output."""
        feedback = Feedback()
        feedback.blue("This is an INFORMATIONAL message.")
        feedback.plain("This is a just a message message.")
        feedback.green("This is a SUCCESS message.")
        feedback.red("This is an ERROR message.")
        feedback.yellow("This is a WARNING message.")
        feedback.hr()

        assert len(feedback.messages) == 6

    def test_heading(self):
        feedback = Feedback()
        feedback.heading("Testing")
        feedback.plain("This is a message.")

        assert len(feedback.messages) == 4

    def test_hr(self):
        """Check that horizontal rules are generated properly."""
        feedback = Feedback()
        feedback.hr(character="=", color=red, size=10)

        # Additional characters are added by the colorization.
        assert len(feedback.messages[0]) == 20

    def test_iter(self):
        """Check that message instances are returned."""
        feedback = Feedback()
        feedback.blue("This is an INFORMATIONAL message.")
        feedback.plain("This is a just a message message.")
        feedback.green("This is a SUCCESS message.")
        feedback.red("This is an ERROR message.")
        feedback.yellow("This is a WARNING message.")
        feedback.hr()

        count = 0
        for message in feedback:
            assert isinstance(message, str) is True
            count += 1

        assert count == 6

    def test_len(self):
        feedback = Feedback()
        feedback.blue("This is an INFORMATIONAL message.")
        feedback.plain("This is a just a message message.")
        feedback.green("This is a SUCCESS message.")
        feedback.red("This is an ERROR message.")
        feedback.yellow("This is a WARNING message.")
        feedback.hr()

        assert len(feedback) == 6

    def test_plain(self):
        feedback = Feedback()
        feedback.plain("This is a message.", prefix="Prefix:", suffix="wow")
        assert feedback.messages[0] == "Prefix: This is a message. wow"

    def test_str(self):
        feedback = Feedback()
        feedback.blue("This is an INFORMATIONAL message.")
        feedback.plain("This is a just a message message.")
        feedback.hr()

        with captured_output() as (output, error):
            print(feedback)
            assert "INFORMATIONAL" in output.getvalue()
            assert "just a message" in output.getvalue()
            assert "---" in output.getvalue()
