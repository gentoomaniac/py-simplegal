"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False
    map.explicit = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    map.connect('/', controller='view', action='viewfolder')
    map.connect('/viewvideo/', controller='view', action='viewvideo')
    map.connect('/viewvideo/*path/', controller='view', action='viewvideo')
    map.connect('/viewfolder/', controller='view', action='viewfolder')
    map.connect('/viewfolder/*path/', controller='view', action='viewfolder')
    map.connect('/getthumbnail/*path/', controller='image', action='getthumbnail')
    map.connect('/getweb/*path/', controller='image', action='getweb')
    map.connect('/getfull/*path/', controller='image', action='getfull')
    map.connect('/getvideo/*path/', controller='video', action='getvideo')
    #map.connect('/{controller}/{action}')
    #map.connect('/{controller}/{action}/{id}')

    return map
