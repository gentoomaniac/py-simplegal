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

    def viewfolder(self, path=''):
        if path:
            abs_path = "%s/%s" % (config['app_conf']['photo_store'], path)
        else:
            abs_path = config['app_conf']['photo_store']
        content = []

        (dirs, files) = h.get_folder_content(abs_path)
        content = dirs + files

        # add template vars
        c.site_name = config['app_conf']['site_name']
        c.site_template = config['app_conf']['site_template']
        c.photo_store = config['app_conf']['photo_store']
        c.folder_preview = config['app_conf']['folder_preview']
        c.current_path = path
        c.paths = h.path_to_array(path)
        c.abspath = abs_path
        c.path = path
        if path:
            c.path += '/'

        c.content = content

        c.thumb_height = config['app_conf']['thumb_height']
        c.thumb_width = config['app_conf']['thumb_width']

        return render("%s/viewfolder.html" % config['app_conf']['site_template'])

