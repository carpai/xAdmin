#!/usr/bin/env python3

from mongokit import Document

class Order(Document):
    structure = {
        'id_str'          : str,
        'user_id'         : str,
        'dealer_id'       : str,
        'good_id'         : list,
        'unit'            : str,
        'counts'          : str,
        'price'           : str,
        'payment'         : str,
        'create_time'     : str,
        'endtime'         : str,

        'status'          : int
    }

    use_dot_notation = True


