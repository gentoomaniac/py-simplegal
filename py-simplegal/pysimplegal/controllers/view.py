import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import config
from pylons import tmpl_context as c

from pysimplegal.lib.base import BaseController, render

import os

import pysimplegal.lib.helpers as h

log = logging.getLogger(__name__)

class ViewController(BaseController):


    def index(self):
        # Return a rendered template
        #return render('/view.mako')
        # or, return a string
        return 'This will be the index'

    def viewfolder(self, path=''):
        abs_path = "%s/%s" % (config['app_conf']['photo_store'], path)
        content = []

        try:
            for file in os.listdir(abs_path):
                if os.path.isdir("%s/%s" % (abs_path, file)):
                    content.append([file, None, None])
                else:
                    content.append(("%s/%s" % (path, file), "/getthumbnail/%s/%s/" % (path, file), "/getweb/%s/%s/" % (path, file)))
        except OSError, e:
            raise e

        c.images = content

        return render('/viewfolder.html')

