import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import config

from pysimplegal.lib.base import BaseController, render

import os
import imghdr
import md5
from PIL import Image, ImageOps

log = logging.getLogger(__name__)

class ViewController(BaseController):


    def index(self):
        # Return a rendered template
        #return render('/view.mako')
        # or, return a string
        return 'This will be the index'

    def viewfolder(self,path=''):
        response.content_type = 'text/plain'
        output = "./%s \n\n" % path
        try:
            for content in os.listdir("%s/%s" % (config['app_conf']['photo_store'], path)):
                output += "%s\n" % content
        except OSError, e:
            output += "Ooops! %s doesn't exist" % config['app_conf']['photo_store']
        return output

    def _create_cached_image(self, path, width, height, quality, targetpath, square=False):
        """ create resized image and write it to disk

            path: abs path to image
            target: abs path to target
        """
        try:
            img_src = Image.open(path)
        except Exception, e:
            raise e

        if square:
            img_out = ImageOps.fit(img_src, (width, height), Image.ANTIALIAS)
        else:
            img_src.thumbnail((width,height), Image.ANTIALIAS)
            img_out = img_src


        # caching
        md5sum = md5.new()
        md5sum.update(path)
        img_cache = "%s/%s_%sx%s.%s" % (targetpath, md5sum.hexdigest(), width, height, img_src.format.lower())
        if not os.path.isfile(img_cache):
            try:
                img_out.save(img_cache, img_src.format, quality=quality)
            except Exception, e:
                raise e

        with open(img_cache, 'rb') as image:
            return (image.read(), img_src.format)

        return (None, None)


    def getthumbnail(self, path):
        """ create thumbnails
        """
        absimagepath = "%s/%s" % (config['app_conf']['photo_store'], path)
        width = int(config['app_conf']['thumb_with'])
        height = int(config['app_conf']['thumb_height'])
        quality = int(config['app_conf']['thumb_quality'])

        (img_data, img_format) = self._create_cached_image(absimagepath, width, height, quality, config['app_conf']['thumb_store'], square=True)

        # prepare response
        response.content_type = 'image/%s' % img_format
        return img_data


    def getweb(self, path):
        """ create resized pictures for showig in first place
        """
        absimagepath = "%s/%s" % (config['app_conf']['photo_store'], path)
        width = int(config['app_conf']['web_with'])
        height = int(config['app_conf']['web_height'])
        quality = int(config['app_conf']['web_quality'])

        (img_data, img_format) = self._create_cached_image(absimagepath, width, height, quality, config['app_conf']['web_store'])

        # prepare response
        response.content_type = 'image/%s' % img_format
        return img_data

