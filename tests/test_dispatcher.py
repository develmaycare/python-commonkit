from commonkit.dispatcher import Signal

# Example Functions


# noinspection PyUnusedLocal
def example_exception_receiver(**kwargs):
    raise NotImplementedError("This receiver always raises an exception.")


# noinspection PyUnusedLocal
def example_fail_receiver(**kwargs):
    return False, "This receiver always fails."


# noinspection PyUnusedLocal
def example_success_receiver(**kwargs):
    return True, "This receiver is always successful."

# Example Classes


class ExampleSender(object):
    pass

# Tests


class TestSignal(object):

    def test_connect(self):
        """Check that signals may be connected under various conditions."""
        my_signal = Signal(arguments=["testing"])

        # No uid or sender.
        my_signal.connect(example_success_receiver)
        count_1 = 1
        assert len(my_signal.receivers) == count_1

        # Might as well check the identifier.
        assert my_signal.receivers[0].identifier is not None
        assert my_signal.receivers[0].callback_id is not None
        assert my_signal.receivers[0].sender_id is not None

        # With uid.
        my_signal.connect(example_fail_receiver, dispatch_uid="my_example_fail_receiver")
        count_2 = 2
        assert len(my_signal.receivers) == count_2

        # With sender.
        my_signal.connect(example_exception_receiver, sender=ExampleSender)
        count_3 = 3
        assert len(my_signal.receivers) == count_3

        # Duplicate.
        my_signal.connect(example_success_receiver)
        assert len(my_signal.receivers) == count_3

        # Duplicate manually uid.
        my_signal.connect(example_fail_receiver, dispatch_uid="my_example_fail_receiver")
        assert len(my_signal.receivers) == count_3

    def test_disconnect(self):
        """Check that signal receivers may be disconnected."""
        my_signal = Signal(arguments=["testing"])

        count_0 = 0

        # Without a sender.
        my_signal.connect(example_success_receiver)
        my_signal.disconnect(example_success_receiver)
        assert len(my_signal.receivers) == count_0

        # With sender.
        my_signal.connect(example_success_receiver, sender=ExampleSender)
        my_signal.disconnect(example_success_receiver, sender=ExampleSender)
        assert len(my_signal.receivers) == count_0

        # With sender and dispatch UID.
        my_signal.connect(example_success_receiver, dispatch_uid="testing_signal_receiver", sender=ExampleSender)
        my_signal.disconnect(example_success_receiver, dispatch_uid="testing_signal_receiver", sender=ExampleSender)
        assert len(my_signal.receivers) == count_0

    def test_get_callbacks(self):
        """Check that getting callbacks work as expected."""
        my_signal = Signal(arguments=["testing"])

        # No sender so should respond to all signals.
        my_signal.connect(example_success_receiver)
        count_1 = 1
        assert len(my_signal.get_callbacks(ExampleSender)) == count_1

        # With sender.
        my_signal.connect(example_fail_receiver, sender=ExampleSender)
        count_2 = 2
        assert len(my_signal.get_callbacks(ExampleSender)) == count_2

    def test_send(self):
        """Check that signals send as expected."""
        my_signal = Signal(arguments=["testing"])

        # No responses because nothing registered.
        count_0 = 0
        responses = my_signal.send(ExampleSender, testing=True)
        assert len(responses) == count_0

        # Successful response.
        my_signal.connect(example_success_receiver, sender=ExampleSender)
        responses = my_signal.send(ExampleSender, testing=True)
        count_1 = 1
        assert len(responses) == count_1

        my_signal.disconnect(example_success_receiver, sender=ExampleSender)

        # Unsuccessful response.
        my_signal.connect(example_fail_receiver, sender=ExampleSender)
        responses = my_signal.send(ExampleSender, testing=True)
        count_1 = 1
        assert len(responses) == count_1

        my_signal.disconnect(example_fail_receiver, sender=ExampleSender)

        # Exception response.
        my_signal.connect(example_exception_receiver, sender=ExampleSender)
        responses = my_signal.send(ExampleSender, testing=True)
        count_1 = 1
        assert len(responses) == count_1
        assert isinstance(responses[0].error, NotImplementedError)
