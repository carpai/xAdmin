from pyramid.view import (view_config, view_defaults, forbidden_view_config)
from pyramid.response import Response
from pyramid.security import (remember, forget)

from pyramid.httpexceptions import HTTPFound

from .dealerM import Dealer
from xadmin.baseSecurity.Utils import sha256HashStr


@view_defaults(renderer='templates/dealerAdmin/index.jinja2')
class DealerReq:
    def __init__(self, request):
        self.request = request
        # Dealer User table handler
        self.request.dbconn.register([Dealer])
        self.dealertb = self.request.db.Dealertb

    @view_config(route_name='dealer')
    @view_config(route_name='dealerslash')
    def index(self):
        login_url = self.request.route_url('dealer_login')
        session = self.request.session
        print(session)
        if session.get('loginuser') == None:
            print("you're not logged in.")
            return HTTPFound(location=login_url)
        else:
            return {}

    @view_config(route_name='dealer_login', renderer='templates/dealerAdmin/login.jinja2')
    def login(self):
        return {}

    #@forbidden_view_config(renderer='static/dealerAdmin/index.jinja2')
    @view_config(route_name='dealer_loginact', renderer='json')
    def loginAction(self):
        request = self.request
        #login_url = request.route_url('dealer_login')

        if 'ajax.login' in request.params:
            print("yeah, this is POST request.")
            login = request.params['username']
            password  = request.params['password']
            session = request.session
            dealer_this = self.dealertb.Dealer.find_one({'loginame': login})
            if not dealer_this:
                return {'status': '2'}
            if dealer_this.passwd == sha256HashStr(password):
                #headers = remember(request, login)
                session['loginuser'] = login
                # login ok.
                return {'status': '1'}
            else:
                session['loginuser'] = None
                return {'status': '0'}
        else:
            # error when login
            print('invalid login post')
            return {'status': '2'}


    @view_config(route_name='dealer_logout')
    def logout(self):
        session = self.request.session
        session['loginuser'] = None
        url = self.request.route_url('dealer')
        return HTTPFound(url)

    @view_config(route_name='dealer_register', renderer='templates/dealerAdmin/register.jinja2')
    def register(self):
        return {'hello': 'hello'}

    @view_config(route_name='dealer_registeract', renderer='json')
    def registerAction(self):
        print("register post requested!")
        request = self.request
        #login_url = request.route_url('dealer_login')
        #referer = request.referer
        #if (not referer) or (referer == login_url):
        #    referer = request.route_url('dealer')
        if 'ajax.register' in request.params:
            print("dealer user register request.")
            username= request.params.get('regname')
            dealerfd = list(self.dealertb.Dealer.find({'loginame': username}))

            if not dealerfd:
                # registry ok
                dealer = self.dealertb.Dealer()
                dealer.loginame = username
                dealer.passwd = sha256HashStr(request.params.get('regpass'))
                dealer.openid = request.params.get('regweixin')
                dealer.email = request.params.get('regmail')
                dealer.active = False
                dealer.save()
                return {'regstatus': '1'}
            else:
                # already registered
                return {'regstatus': '2'}
        else:
            print("It's not a valid register post")
            # no a valid registry request
            return {'regstatus': '0'}

    """
       Content Request Handle
            ['dealerct_dashboard', '/dealerAdmin/dealerct_dashboard.ct'],
            ['dealerct_oderman', '/dealerAdmin/dealerct_orderman.ct'],
            ['dealerct_productman', '/dealerAdmin/dealerct_productman.ct'],
            ['dealerct_storeinfo', '/dealerAdmin/dealerct_storeinfo.ct'],
    """
    @view_config(route_name='dealerct_dashboard', renderer='templates/dealerAdmin/dashboard.jinja2')
    def dashboard(self):
        session = self.request.session
        if session.get('loginuser') != None:
            return {'header':'欢迎使用三驾马车平台', 'smallheader': '工作面板'}
        else:
            return Response('forbidden')

    @view_config(route_name='dealerct_oderman', renderer='templates/dealerAdmin/orderlist.jinja2')
    def oderlist(self):
        session = self.request.session
        if session.get('loginuser') != None:
            return Response('Not found!')
        else:
            return Response('forbidden')

    @view_config(route_name='dealerct_productman', renderer='templates/dealerAdmin/product.jinja2')
    def product(self):
        session = self.request.session
        if session.get('loginuser') != None:
            return Response('Not found!')
        else:
            return Response('forbidden')

    @view_config(route_name='dealerct_storeinfo', renderer='templates/dealerAdmin/storeinfo.jinja2')
    def store(self):
        session = self.request.session
        if session.get('loginuser') != None:
            return Response('Not found!')
        else:
            return Response('forbidden')

    @view_config(route_name='dealerct_userinfo', renderer='templates/dealerAdmin/userinfo.jinja2')
    def store(self):
        session = self.request.session
        if session.get('loginuser') != None:
            return {'title': "个人信息配置"}
        else:
            return Response('forbidden')

