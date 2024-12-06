from cli_support import graceful_keyboard_interrupt, debugger_on_error


class SingletonMetaclass(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
    
    
class GracefulInterruptMetaclass(type):
    def __new__(cls, name, bases, attrs):
        # Wrap all public methods with graceful_keyboard_interrupt
        for key, value in attrs.items():
            if callable(value) and not key.startswith('_'):
                attrs[key] = graceful_keyboard_interrupt(value)
        return super().__new__(cls, name, bases, attrs)
    
    
class DebuggerOnErrorMetaclass(type):
    def __new__(cls, name, bases, attrs):
        for key, value in attrs.items():
            if callable(value) and not key.startswith('_'):
                attrs[key] = debugger_on_error(value)
        return super().__new__(cls, name, bases, attrs)




class LoggedMetaclass(type):
    """Metaclass that logs all method calls for a class"""
    def __new__(cls, name, bases, attrs):
        # Wrap callable methods with logging
        for key, value in attrs.items():
            if callable(value) and not key.startswith('_'):
                attrs[key] = cls.log_call(value)
        return super().__new__(cls, name, bases, attrs)
    
    @staticmethod
    def log_call(func):
        def wrapper(*args, **kwargs):
            print(f'Calling: {func.__name__}')
            result = func(*args, **kwargs)
            print(f'Finished: {func.__name__}')
            return result
        return wrapper