#!/usr/bin/env python3

#import datetime
from mongokit import Document

class User(Document):
    structure = {
        'name' : str,
        'agende' : str,
        'age' : int,
        'height' : float,
    }

    validators = {
        'age': lambda x: x > 18,
        'agende': lambda x: x == 'boy'
    }

    default_values = {
        'age' : 17,
        'agende': 'girl',
    }

    use_dot_notation = True


