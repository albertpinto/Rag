

def singleton(cls):
    """
    Decorator that makes a class follow the Singleton design pattern.
    In other words, there can be at-most one object instance of the class,
    and the repeated call to the constructor will yield the same object instance.
    """
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance