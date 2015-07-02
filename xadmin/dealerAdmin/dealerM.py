#!/usr/bin/env python3

from mongokit import Document

class Dealer(Document):
    structure = {
        'loginame'       : str,
        'active'         : bool,
        'passwd'         : str,
        'openid'         : str,
        'mobile'         : str,
        'email'          : str,
        'avatar'         : str,
        'nickname'       : str,

        # .....
        'service_time'   : str,
        'store_name'     : str,
        'store_addr'     : str,
        'service_type'   : str,
        'store_describe' : str,
        'store_image'    : list,
        'store_location' : str
    }

    validators = {
        'mobile': lambda x: int(x) > 10000000000,
    }

    default_values = {

    }

    use_dot_notation = True


