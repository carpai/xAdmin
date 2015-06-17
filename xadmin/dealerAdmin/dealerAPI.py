from pyramid_rpc.jsonrpc import jsonrpc_method
from .dealerM import Dealer

@jsonrpc_method(endpoint='dealerApi')
def checkUser(self, name):
    self.dbconn.register([Dealer])
    dealertb = self.db.Dealertb

    dealer = list(dealertb.Dealer.find({'loginame': name}))
    if not dealer:
        return False
    else:
        return True
