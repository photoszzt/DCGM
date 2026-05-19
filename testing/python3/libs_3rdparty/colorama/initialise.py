import atexit
import sys

from .ansitowin32 import AnsiToWin32


orig_stdout = sys.stdout
orig_stderr = sys.stderr

wrapped_stdout = sys.stdout
wrapped_stderr = sys.stderr

atexit_done = False


def reset_all() -> None:
    AnsiToWin32(orig_stdout).reset_all()


def init(autoreset: bool=False, convert=None, strip=None, wrap: bool=True) -> None:

    if not wrap and any([autoreset, convert, strip]):
        raise ValueError('wrap=False conflicts with any other arg=True')

    global wrapped_stdout, wrapped_stderr
    sys.stdout = wrapped_stdout = \
        wrap_stream(orig_stdout, convert, strip, autoreset, wrap)
    sys.stderr = wrapped_stderr = \
        wrap_stream(orig_stderr, convert, strip, autoreset, wrap)

    global atexit_done
    if not atexit_done:
        atexit.register(reset_all)
        atexit_done = True


def deinit() -> None:
    sys.stdout = orig_stdout
    sys.stderr = orig_stderr


def reinit() -> None:
    sys.stdout = wrapped_stdout
    sys.stderr = wrapped_stdout


def wrap_stream(stream, convert, strip, autoreset: bool, wrap: bool):
    if wrap:
        wrapper = AnsiToWin32(stream,
            convert=convert, strip=strip, autoreset=autoreset)
        if wrapper.should_wrap():
            stream = wrapper.stream
    return stream


