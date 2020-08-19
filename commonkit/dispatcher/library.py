# Classes


class Receiver(object):
    """Receiver instances provide a descriptor for storing data regarding a signal's callbacks."""

    def __init__(self, callback, identifier):
        """Initialize a receiver.

        :param callback: The function to call.

        :param identifier: The unique receiver identity created when ``Signal.connect()`` is called.
        :type identifier: tuple(int, int)
        """
        self.callback = callback
        self.identifier = identifier

    @property
    def callback_id(self):
        """Get the unique ID of the callback."""
        return self.identifier[0]

    @property
    def sender_id(self):
        """Get the unique ID of the sender."""
        return self.identifier[1]


class Response(object):
    """Encapsulate the result of sending a signal."""

    def __init__(self, success, error=None, output=None):
        """Initialize a response.

        :param success: Indicates whether the callback reported success.
        :type success: bool

        :param error: The error, if any, that was raised by the callback.
        :type error: Exception

        :param output: The output of the callback, if any.
        """
        self.error = error
        self.output = output
        self.success = success


class Signal(object):
    """A signal is used to send messages to receivers."""

    def __init__(self, arguments=None):
        """Initialize the signal.

        :param arguments: A list of arguments the signal will send to callbacks.
        :type arguments: list

        """
        self.arguments = arguments
        self.receivers = list()

    def connect(self, callback, dispatch_uid=None, sender=None):
        """Connect to the signal.

        :param callback: The callback function that listens for the signal.

        :param dispatch_uid: A unique ID for the callback. If omitted, a unique ID will be created.
        :type dispatch_uid: str || unicode

        :param sender: The class that sends the signal. ``None`` means the callback will listen for all signals.

        """
        if dispatch_uid is not None:
            identifier = (dispatch_uid, id(sender))
        else:
            identifier = (id(callback), id(sender))

        for receiver in self.receivers:
            if identifier == receiver.identifier:
                break
        else:
            self.receivers.append(Receiver(callback, identifier))

    def disconnect(self, callback=None, sender=None, dispatch_uid=None):
        """Disconnect a previously registered callback.

        :param callback: The callback function that was registered for the signal. ``None`` if ``dispatch_uid`` is
                         provided.

        :param dispatch_uid: The unique ID originally given for the callback. If omitted, ``callback`` must be supplied.
        :type dispatch_uid: str || unicode

        :param sender: The class for which the callback is listening, if any.

        """
        if dispatch_uid is not None:
            identifier = (dispatch_uid, id(sender))
        else:
            identifier = (id(callback), id(sender))

        for index in range(len(self.receivers)):
            receiver = self.receivers[index]
            if identifier == receiver.identifier:
                del self.receivers[index]
                break

    def get_callbacks(self, sender):
        """Get the receivers to be called for the given sender.

        :param sender: The class that is sending the signal.

        :rtype: list

        """
        no_sender_id = id(None)
        current_sender_id = id(sender)

        callbacks = list()
        for receiver in self.receivers:
            if receiver.sender_id == no_sender_id or current_sender_id == receiver.sender_id:
                callbacks.append(receiver.callback)

        return callbacks

    def send(self, sender, **arguments):
        """Send the signal.

        :param sender: The class that is sending the signal.

        :param arguments: The keyword arguments sent by the sender.

        :rtype: list[Response]

        """
        responses = list()

        if len(self.receivers) == 0:
            return responses

        for callback in self.get_callbacks(sender):

            # noinspection PyBroadException
            try:
                error = None
                success, output = callback(**arguments)
            except Exception as e:
                error = e
                output = None
                success = False

            responses.append(Response(success, error=error, output=output))

        return responses
