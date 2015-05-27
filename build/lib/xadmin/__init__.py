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
    config.add_subscriber(add_mongokit, NewRequest)

    # static files
    config.add_static_view('static', 'static', cache_max_age=3600)

    #
    # applications
    #
    def addApp(package):
        # load subpackage url dispatch
        import importlib
        subpkgurls = package + '.urls'
        urlpatterns = importlib.import_module(subpkgurls).urlpatterns
        print(urlpatterns)
        for i in range(len(urlpatterns)):
            config.add_route(urlpatterns[i][0], urlpatterns[i][1])
        # scan subpackage view
        config.scan(package)

    # register apps
    addApp('xadmin.app1')
    addApp('xadmin.app2')

    return config.make_wsgi_app()
