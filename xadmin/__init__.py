from pyramid.config import Configurator
from pyramid.events import (subscriber, NewRequest)
from mongokit import Connection

def main(global_config, **settings):
    """
        This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    """
        MongoDB conn
    """
    mongourl = settings['mongodb.conn']
    mongodbn = settings['mongodb.name']
    dbconn = Connection(mongourl)
    dbhdl = dbconn[mongodbn]

    # add mongo ming session handler to every request object.
    def add_mongokit(event):
        req = event.request
        # add (dbconn, db) to request object
        req.dbconn = dbconn
        req.db = dbhdl

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('say', '/saytxt')
    config.add_route('dict', '/dict')
    config.add_route('getusr', '/getusr')
    config.add_route('addusr', '/adduser')
    config.add_route('addusraction', '/addusraction')
    config.add_subscriber(add_mongokit, NewRequest)
    config.scan('.views')

    return config.make_wsgi_app()
