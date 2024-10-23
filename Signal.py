# Simple Event System
class Signal:
    def __init__(self):
        self._subscribers = []

    def connect(self, subscriber):
        if isinstance(subscriber, list):
            for sub in subscriber:
                self._subscribers.append(sub)
        else:
            self._subscribers.append(subscriber)

    def emit(self, *args, **kwargs):
        for subscriber in self._subscribers:
            subscriber(*args, **kwargs)
