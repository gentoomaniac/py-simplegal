import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import config

from pysimplegal.lib.base import BaseController, render

log = logging.getLogger(__name__)

class VideoController(BaseController):

    def getvideo(self, path):
        abspath = "%s/%s" % (config['app_conf']['photo_store'], path)
        with open(abspath, 'rb') as image:
            response.content_type = 'video/x-matroska'
            return image.read()
        return None
