import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import config

from pysimplegal.lib.base import BaseController, render

import os
from PIL import Image, ImageOps
import imghdr

import pysimplegal.lib.helpers as h

log = logging.getLogger(__name__)

class ImageController(BaseController):

    def _create_cached_image(self, path, width, height, quality, targetpath, square=False):
        """ create resized image and write it to disk

            path: abs path to image
            target: abs path to target
        """
        img_cache = "%s/%s" % (targetpath, h.get_thumb_filename(path))
        img_type = imghdr.what(path)
        # check if there is a cached file, if yes we can skipp nearly everything
        # skip directly if it is a a gif image
        # and we're not doing a thumbnail
        if not os.path.isfile(img_cache) and (img_type != 'gif' or square):
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
            img_cache = "%s/%s" % (targetpath, h.get_thumb_filename(path))
            try:
                img_out.save(img_cache, img_src.format, quality=quality)
            except Exception, e:
                raise e


        # either we had a cached image or the work is done, so read the
        # thumb for the correct filetype and return everything
        if img_type != 'gif' or square:
            file_to_return = img_cache
            img_thumb = Image.open(img_cache)
            file_format = img_thumb.format
        else:
            file_to_return = path
            file_format = 'GIF'

        with open(file_to_return, 'rb') as image:
            return (image.read(), file_format)

        return (None, None)


    def getthumbnail(self, path):
        """ create thumbnails
        """
        absimagepath = "%s/%s" % (config['app_conf']['photo_store'], path)
        width = int(config['app_conf']['thumb_width'])
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
        width = int(config['app_conf']['web_width'])
        height = int(config['app_conf']['web_height'])
        quality = int(config['app_conf']['web_quality'])

        (img_data, img_format) = self._create_cached_image(absimagepath, width, height, quality, config['app_conf']['web_store'])

        # prepare response
        response.content_type = 'image/%s' % img_format
        return img_data

    def getfull(self, path):
        absimagepath = "%s/%s" % (config['app_conf']['photo_store'], path)
        try:
            img_src = Image.open(absimagepath)
        except Exception, e:
            raise e

        with open(absimagepath, 'rb') as image:
            response.content_type = 'image/%s' % img_src.format
            return image.read()
        return None
