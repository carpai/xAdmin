from pyramid_rpc.jsonrpc import jsonrpc_method
from .dealerM import Dealer
from .productM import Product

@jsonrpc_method(endpoint='dealerApi')
def checkUser(self, name):
    self.dbconn.register([Dealer])
    dealertb = self.db.Dealertb

    dealer = list(dealertb.Dealer.find({'loginame': name}))
    if not dealer:
        return False
    else:
        return True


@jsonrpc_method(endpoint='dealerApi')
def delProduct(self, name):
    session = self.session
    if session.get('loginuser') != None:
        self.dbconn.register([Product])
        producttb = self.db.Producttb
        print(name)
        product = producttb.Product.find_one({'product_name':name})
        if not product:
            return False
        else:
            print(dir(producttb.Product))
            product.delete()
            #producttb.Product.delete()
            return True