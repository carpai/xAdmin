from pyramid.view import (view_config, view_defaults)
from pyramid.response import Response


@view_config(route_name='home', renderer='templates/test.jinja2')
def home(self, request):
    return {'project': 'xadmin'}

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









