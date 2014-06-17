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

    def _set_global_template_vars(self, path):
        if path:
            abs_path = "%s/%s" % (config['app_conf']['photo_store'], path)
        else:
            abs_path = config['app_conf']['photo_store']
        c.site_name = config['app_conf']['site_name']
        c.site_author = config['app_conf']['site_author']
        c.site_version = config['app_conf']['site_version']
        c.site_template = config['app_conf']['site_template']
        c.photo_store = config['app_conf']['photo_store']
        c.folder_preview = config['app_conf']['folder_preview']
        if path:
            c.path = "%s/" % path
        else:
            c.path = path
        c.paths = h.path_to_array(path)
        c.thumb_height = config['app_conf']['thumb_height']
        c.thumb_width = config['app_conf']['thumb_width']
        c.thumbs_per_page = int(config['app_conf']['site_max_per_page'])
        c.abspath = abs_path
        if 'page' in request.GET:
            c.current_page = int(request.GET['page'])
        else:
            c.current_page = 1


    def viewfolder(self, path='', page=1):
        if path:
            abs_path = "%s/%s" % (config['app_conf']['photo_store'], path)
        else:
            abs_path = config['app_conf']['photo_store']
        content = []

        (dirs, files) = h.get_folder_content(abs_path)
        content = dirs + files

        # add template vars
        self._set_global_template_vars(path=path)
        c.content = content
        c.content_len = len(content)

        return render("%s/viewfolder.html" % config['app_conf']['site_template'])

    def viewvideo(self, path=''):
        """ parse template to provide videoplayer iframe content
        """
        if path:
            abs_path = "%s/%s" % (config['app_conf']['photo_store'], path)
        else:
            abs_path = config['app_conf']['photo_store']


        # add template vars
        self._set_global_template_vars(path=path)
        c.mime = h.get_file_type(abs_path)['mime']

        return render("%s/viewvideo.html" % config['app_conf']['site_template'])
