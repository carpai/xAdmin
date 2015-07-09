from pyramid.view import (view_config, view_defaults, forbidden_view_config)
from pyramid.response import Response
from pyramid.security import (remember, forget)

from pyramid.httpexceptions import HTTPFound

from .dealerM import Dealer
from xadmin.baseSecurity.Utils import sha256HashStr

import os, time


@view_defaults(renderer='templates/dealerAdmin/index.jinja2')
class DealerReq:
    def __init__(self, request):
        self.request = request
        # Dealer User table handler
        self.request.dbconn.register([Dealer])
        self.dealertb = self.request.db.Dealertb

    def dealerCheckDefault(self, dealer):
        dealer_this = dealer
        if not dealer_this.avatar:
            dealer_this.avatar = "avatar.png"
        if not dealer_this.mobile:
            dealer_this.mobile = 'notset'
        if not dealer_this.email:
            dealer_this.email = 'notset'
        if not dealer_this.openid:
            dealer_this.openid = 'notset'
        if not dealer_this.nickname:
             dealer_this.nickname = '三驾马车商家'
        return dealer_this

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
            currDealer = session.get('loginuser')
            if currDealer != None:
                dealer_this = self.dealertb.Dealer.find_one({'loginame': currDealer})
                dealer_this = self.dealerCheckDefault(dealer_this)
            return {'User': dealer_this}

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
            return {}
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
            return {}
        else:
            return Response('forbidden')

    @view_config(route_name='dealerct_storeinfo', renderer='templates/dealerAdmin/storeinfo.jinja2')
    def store(self):
        session = self.request.session
        currDealer = session.get('loginuser')
        if currDealer != None:
            timestamp = str(time.time())
            dealer_this = self.dealertb.Dealer.find_one({'loginame': currDealer})
            return {'timestamp': timestamp, 'storeimglist': dealer_this.store_image,
                    'count': len(dealer_this.store_image)}
        else:
            return Response('forbidden')

    @view_config(route_name='dealterct_storepic', renderer='json')
    def storePicUpload(self):
        session = self.request.session
        currDealer = session.get('loginuser')
        if currDealer != None:
            if self.request.method == 'POST':
                images_data = self.request.params
                counts = len(images_data)
                for i in range(counts):
                    img = images_data.getall('file_data')[i]
                    dealerpic_path = 'xadmin/static/Images/Dealer/%s' % (session.get('loginuser'))
                    if not os.path.exists(dealerpic_path):
                        os.makedirs(dealerpic_path, exist_ok=True)
                    open('%s/%d.jpg' %(dealerpic_path, i), 'wb').write(img.file.read())
                prev_list = []
                img_list = []
                for i in range(counts):
                    imgurl = "/static/Images/Dealer/" + session.get('loginuser') + "/" + str(i) + ".jpg"
                    prev_list.append( "<img src='" + imgurl + "?" + str(time.time()) + \
                                      "' class='file-preview-image' alt='" \
                                      + str(i) +"' title='" + str(i) + "'>")
                    img_list.append(imgurl)
                    #print(img.filename)

                dealer_this = self.dealertb.Dealer.find_one({'loginame': currDealer})
                dealer_this.store_image = img_list
                dealer_this.save()
                return {'initialPreview': prev_list}
                #return {'error': 'You have faced errors in 4 files.', 'errorkeys': [0, 3, 4, 5]}
        else:
            return Response('forbidden')



    @view_config(route_name='dealerct_userinfo', renderer='templates/dealerAdmin/userinfo.jinja2')
    def userinfo(self):
        session = self.request.session
        currDealer = session.get('loginuser')
        if currDealer != None:
            dealer_this = self.dealertb.Dealer.find_one({'loginame': currDealer})
            dealer_this = self.dealerCheckDefault(dealer_this)
            return {'title': "个人信息配置", 'User': dealer_this}
        else:
            return Response('forbidden')

