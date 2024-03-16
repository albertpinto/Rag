#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2023.  SupportVectors AI Lab
#   This code is part of the training material, and therefore part of the intellectual property.
#   It may not be reused or shared without the explicit, written permission of SupportVectors.
#  
#   Use is limited to the duration and purpose of the training at SupportVectors.
#  
#   Author: Asif Qamar
#  -------------------------------------------------------------------------------------------------



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