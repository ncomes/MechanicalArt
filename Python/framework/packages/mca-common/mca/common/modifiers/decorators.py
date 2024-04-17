#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains the mca decorators at a base python level
"""

# mca python imports
import os
import sys
import time
import threading
from functools import wraps
# software specific imports

# mca python imports
from mca.common import log
from mca.common.utils import process, strings
from mca.common.tools.dcctracking import dcc_tracking


logger = log.MCA_LOGGER


def add_metaclass(metaclass):
    """
    Decorators that allows to create a class using a metaclass
    https://github.com/benjaminp/six/blob/master/six.py
    """

    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        if hasattr(cls, '__qualname__'):
            orig_vars['__qualname__'] = cls.__qualname__
        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper


def timestamp(f):
    """
    Function decorator that gets the elapsed time with a more descriptive output.

    :param callable f: decorated function
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = f(*args, **kwargs)
        function_name = f.func_name or f.__name__
        logger.info('<{}> Elapsed time : {}'.format(function_name, time.time() - start_time))
        return res
    return wrapper


def repeater(interval, limit=-1):
    """
    A function interval decorator based on:
        http://stackoverflow.com/questions/5179467/equivalent-of-setinterval-in-python

    :param: int interval: interval (in seconds) between function invocations.
    :param int limit: limit to the number of function invocations; -1 represents infinity.
    :return: decorator with a closure around the original function and the Python threading. Thread used to invoke it.
    """

    def actual_decorator(fn):

        def wrapper(*args, **kwargs):

            class RepeaterTimerThread(threading.Thread):
                def __init__(self):
                    threading.Thread.__init__(self)
                    self._event = threading.Event()

                def run(self):
                    i = 0
                    while i != limit and not self._event.is_set():
                        self._event.wait(interval)
                        fn(*args, **kwargs)
                        i += 1
                    else:
                        if self._event:
                            self._event.set()

                def stopped(self):
                    return not self._event or self._event.is_set()

                def pause(self):
                    self._event.set()

                def resume(self):
                    self._event.clear()

                def stop(self):
                    self._event.set()
                    self.join()

            token = RepeaterTimerThread()
            token.daemon = True
            token.start()
            return token

        return wrapper

    return actual_decorator


def error(func):
    """
    Function decorator used to handle exceptions and report them to the user.
    """

    @wraps(func)
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            # remove decorator(s) from the traceback stack
            exc_type, exc_value, exc_traceback = sys.exc_info()
            if exc_traceback:
                while 'wrapper' in exc_traceback.tb_frame.f_code.co_name:
                    tb = exc_traceback.tb_next
                    if not tb:
                        break
                    exc_traceback = exc_traceback.tb_next

            logger.error(exc_value.__str__(), exc_info=(exc_type, exc_value, exc_traceback))

            from mca.common.qt import api as qt
            # making sure the ui popup is ignored in non-gui threads
            app = qt.QApplication.instance()
            if app and qt.QThread.currentThread() == app.thread():
                if qt.QApplication.instance():
                    qt.messagebox_critical('MAT DCC Framework', exc_value.__str__())

    return func_wrapper


def debug(func):
    """
    Function decorator used to log a debug message.
    """

    DEBUG_MESSAGE = '{trace}(): Executed in {time} secs.'
    DEBUG_SEPARATOR = ' --> '

    @wraps(func)
    def func_wrapper(*args, **kwargs):

        # get the callee, and the executing time and info
        t = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            if args and hasattr(args[0], '__class__'):
                name = f'{args[0].__class__}.{func.__name__}'
            else:
                name = func.__name__

            trace = [name, ]

            logger.debug(DEBUG_MESSAGE.format(trace=DEBUG_SEPARATOR.join(trace), time=time.time() - t))

    return func_wrapper


def track_fnc(fn):
    """
    Function decorator that exports data to a google sheets for tracking functions.

    :param callable fn: decorated function.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            process.cpu_threading(dcc_tracking.ddc_tool_entry(fn))
            try:
                result = fn(*args, **kwargs)
            except Exception:
                raise
            return result
        except Exception:
            raise

    return wrapper

def abstractmethod(fn):
    """
    The decorated function should be overridden by a software specific module.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        msg = 'Abstract implementation has not been overridden.'
        mode = os.getenv('ABSTRACT_METHOD_MODE', None)
        if not mode or mode == 'raise':
            raise NotImplementedError(strings.debug_object_string(fn, msg))
        elif mode == 'warn':
            logger.warning(strings.debug_object_string(fn, msg))
        return fn(*args, **kwargs)

    return wrapper