"""
Module that contains the mca decorators at a base python level
"""

# python imports
# software specific imports
# mca python imports


class Singleton(type):
    """
    Singleton decorator as metaclass. Should be used in conjunction with add_metaclass function of this module

    @add_metaclass(Singleton)
    class MyClass(BaseClass, object):
    """
    _instances = {}
    
    def __new__(meta, name, bases, clsdict):
        if any(isinstance(cls, meta) for cls in bases):
            raise TypeError('Cannot inherit from singleton class')
        clsdict['_instance'] = None
        return super(Singleton, meta).__new__(meta, name, bases, clsdict)

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class _Singleton(type):
    """ A metaclass that creates a Singleton base class when called. """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# For use simply inherit this class.
class SimpleSingleton(_Singleton('SingletonMeta', (object,), {})): pass


def clear_cls(class_inst):
    """
    Removes a class instance from the singleton.
    
    :param class_inst:
    :return: If True it successfully removes the class instance from the singleton
    :rtype: bool
    """
    
    for name, inst in Singleton._instances.items():
        if inst == class_inst:
            Singleton._instances.pop(name)
            return True
    return False


def teardown():
    """
    Removes all the classes from a Singleton
    """
    
    Singleton._instances = {}
