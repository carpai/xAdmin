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
        if not self.logged_in:
            return HTTPFound(location=login_url)
        else:
            return {}

    @view_config(route_name='dealer_login', renderer='templates/dealerAdmin/login.jinja2')
    @forbidden_view_config(renderer='static/dealerAdmin/index.jinja2')
    def login(self):
        request = self.request
        login_url = request.route_url('dealer_login')
        referer = request.referer
        if (not referer) or (referer == login_url):
            referer = '/dealerAdmin'
        came_from = request.params.get('came_from', referer)
        message = ''
        login = ''
        password = ''
        if 'form.login' in request.params:
            print("yeah, this is POST request.")
            login = request.params['login']
            password  = request.params['password']
            if USERS.get(login) == password:
                headers = remember(request, login)
                return HTTPFound(location = came_from, headers = headers)
            message = 'Failed on login'
        else:
            print("yeah, this is get request.")
        return dict(
            name = 'login',
            message = message,
            url = request.application_url + '/login',
            came_from = came_from,
            login = login,
            password = password
        )

    @view_config(route_name='dealer_logout')
    def logout(self):
        request = self.request
        headers = forget(request)
        url = request.route_url('dealer')
        return HTTPFound(location=url, headers=headers)

    @view_config(route_name='dealer_register', renderer='templates/dealerAdmin/register.jinja2')
    def register(self):
        return {'hello': 'hello'}

