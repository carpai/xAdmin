from pyramid.view import (view_config, view_defaults, forbidden_view_config)
from pyramid.response import Response

from pyramid.httpexceptions import HTTPFound

from pyramid.security import (remember, forget)
from ..security import  USERS

@view_defaults(renderer='templates/home.jinja2')
class Home:
    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid

    @view_config(route_name='home')
    def home(self):
        login_url = self.request.route_url('login')
        if not self.logged_in:
            return {'name': 'Home View, You are not logged in'}
        else:
            return {'name': 'Home View', 'User': self.logged_in}

    @view_config(route_name='login', renderer='templates/login.jinja2')
    @forbidden_view_config(renderer='templates/login.jinja2')
    def login(self):
        request = self.request
        login_url = request.route_url('login')
        referer = request.referer
        if (not referer) or (referer == login_url):
            referer = '/'
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

    @view_config(route_name='logout')
    def logout(self):
        request = self.request
        headers = forget(request)
        url = request.route_url('home')
        return HTTPFound(location=url, headers=headers)



# json, jsonp, string
@view_config(route_name='dict', renderer='string')
def dictex(self, request):
    return {'a1': 'a1text', 'b2': 2}

@view_defaults(renderer='templates/say.jinja2')
class another:
    def __init__(self, request):
         self.request = request

    @view_config(route_name='say')
    def say(self):
        return {'text': 'Hooo'}









