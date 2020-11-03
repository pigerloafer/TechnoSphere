from time import sleep
import functools
import signal


class TimeoutException(RuntimeError):
    def __init__(self, message=None):
        super().__init__(message)


def handler(signum, frame):
    raise TimeoutException("Timed out")


def timeout(seconds):
    def decorator(func):
        if(seconds is None or seconds <= 0):
            return func

        @functools.wraps(func)
        def wrapper(*args, **argv):
            signal.signal(signal.SIGALRM, handler)
            signal.setitimer(signal.ITIMER_REAL, seconds)
            result = func(*args, **argv)
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, signal.SIG_DFL)
            return result
        return wrapper
    return decorator
