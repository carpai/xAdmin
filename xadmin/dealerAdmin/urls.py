# dealerAdmin url dispatch
urlpatterns = [
    ['dealer', '/dealerAdmin'],
    ['dealerslash', 'dealerAdmin/'],
    ['dealer_login', '/dealerAdmin/login'],
    ['dealer_loginact', '/dealerAdmin/login.do'],
    ['dealer_logout', '/dealerAdmin/logout'],
    ['dealer_register', '/dealerAdmin/register'],
    ['dealer_registeract', '/dealerAdmin/register.do'],
    ['product_addact','/dealerAdmin/addproduct.do'],
    # content urls
    ['dealerct_dashboard', '/dealerAdmin/dealerct_dashboard.ct'],
    ['dealerct_oderman', '/dealerAdmin/dealerct_orderlist.ct'],
    ['dealerct_productman', '/dealerAdmin/dealerct_product.ct'],
    ['dealerct_storeinfo', '/dealerAdmin/dealerct_storeinfo.ct'],
    ['dealerct_userinfo', '/dealerAdmin/dealerct_userinfo.ct'],

    # upload pics
    ['dealterct_storepic', '/dealerAdmin/dealerct_storepic.up'],
]
