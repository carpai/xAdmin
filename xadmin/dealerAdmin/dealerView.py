from pyramid.view import (view_config, view_defaults, forbidden_view_config)
from pyramid.response import Response

from pyramid.httpexceptions import HTTPFound

from pyramid.security import (remember, forget)
from ..security import  USERS

@view_defaults(renderer='templates/dealerAdmin/index.jinja2')
class Dealer:
    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid

    @view_config(route_name='dealer')
    def index(self):
        login_url = self.request.route_url('dealer_login')
        session = self.request.session
        if session['loginuser'] == None:
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
        login_url = request.route_url('dealer_login')
        referer = request.referer
        if (not referer) or (referer == login_url):
            referer = request.route_url('dealer')
        # get camefrom from html page settings, if null ,use referer.
        # came_from = request.params.get('came_from', referer)
        came_from = referer
        message = ''
        login = ''
        password = ''
        if 'form.login' in request.params:
            print("yeah, this is POST request.")
            login = request.params['username']
            password  = request.params['password']
            session = request.session
            if USERS.get(login) == password:
                headers = remember(request, login)

                session['loginuser'] = loginheaders=headers
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

