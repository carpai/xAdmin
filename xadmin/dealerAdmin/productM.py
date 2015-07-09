#!/usr/bin/env python3

from mongokit import Document

class Product(Document):
    structure = {
        'dealer_id'      : str,
        'product_name'   : str,
        'catalog'        : str,
        'images'         : str,
        'discribe'       : str,
        'price'          : str,
        'date'           : str
    }

    validators = {

    }

    default_values = {

    }

    use_dot_notation = True