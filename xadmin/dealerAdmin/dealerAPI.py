from pyramid_rpc.jsonrpc import jsonrpc_method
from ..security import  USERS

@jsonrpc_method(endpoint='dealerApi')
def checkUser(self, name):
    if name in USERS:
        return True
    else:
        return False
