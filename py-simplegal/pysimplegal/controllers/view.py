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
        folder_data = []

        (folders, files) = h.get_images_from_folder(abs_path)
        if path:
            folders = ["%s/%s" % (path, folder) for folder in folders]
            files = ["%s/%s" % (path, filename) for filename in files]

        for folder in folders:
            if config['app_conf']['folder_preview']:
                (fol, fil) = h.get_images_from_folder("%s/%s" % (config['app_conf']['photo_store'], folder))
                folder_data.append([folder, fil])
            else:
                folder_data.append([folder, []])

        # add template vars
        c.site_name = config['app_conf']['site_name']
        c.current_path = path
        c.paths = h.path_to_array(path)

        c.images = files
        c.folders = folder_data

        c.thumb_height = config['app_conf']['thumb_height']
        c.thumb_width = config['app_conf']['thumb_width']

        return render('/viewfolder.html')

