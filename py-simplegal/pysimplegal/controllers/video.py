import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import config

from pysimplegal.lib.base import BaseController, render

import pysimplegal.lib.helpers as h

log = logging.getLogger(__name__)

class VideoController(BaseController):

    def getvideo(self, path):
        import shutil
        abspath = "%s/%s" % (config['app_conf']['photo_store'], path)

        response.content_type = h.get_file_type(abspath)['mime']
        with open(abspath, 'r') as f:
            shutil.copyfileobj(f, response)
