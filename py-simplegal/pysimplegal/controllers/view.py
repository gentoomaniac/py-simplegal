import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import config

from pysimplegal.lib.base import BaseController, render

log = logging.getLogger(__name__)

class ViewController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/view.mako')
        # or, return a string
        return 'This will be the index'

    def viewfolder(self,path=''):
        response.content_type = 'text/plain'
        output = "./%s \n" % path
        output += "%s\n" % config['app_conf'].keys()
        for key in config['app_conf'].keys():
            output += "%s = %s\n" % (key, config['app_conf'][key])
        return output
