from pyramid.view import (view_config, view_defaults)
from pyramid.response import Response

from .model1 import User

"""
  Mongokit operation.
"""
@view_config(route_name='getusr', renderer='templates/getuser.jinja2')
def getUser(self, request):
    request.dbconn.register([User])
    usrtb = request.db.Usertb

    # real query
    usrs = usrtb.User.find()
    return {'Users': list(usrs)}

@view_config(request_method='POST', route_name='addusraction')
def addUserAction(self, request):
    if 'addUsersubmit'in request.params:
        if request.params.has_key('name'):
            name = request.params.get('name')
            gender = request.params['gender']
            age = request.params['age']
            height = request.params['height']

            # register 'User' model
            request.dbconn.register([User])
            # ready to operation the Usertb
            usrtb = request.db.Usertb
            usr = usrtb.User()
            usr.name = name
            usr.gender = gender
            usr.age = int(age)
            usr.height = float(height)
            usr.save()
            return Response(body='User add sucessfull!', content_type='text/plain')
        else:
            return Response(body='User add failed!', content_type='text/plain')
    else:
        return Response(body='Server error: No data posted in.', content_type='text/plain')



@view_config(route_name='addusr', renderer='templates/adduser.jinja2')
def addUser(self, request):
    return {}
