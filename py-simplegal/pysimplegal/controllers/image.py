import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons import config

from pysimplegal.lib.base import BaseController, render

import os
from PIL import Image, ImageOps, ExifTags
import imghdr

import pysimplegal.lib.helpers as h

log = logging.getLogger(__name__)

class ImageController(BaseController):

    def _create_cached_image(self, path, width, height, quality, targetpath, square=False, exif_rotate=True):
        """ create resized image and write it to disk

            path: abs path to image
            target: abs path to target
        """
        img_cache = "%s/%s" % (targetpath, h.get_thumb_filename(path))
        try:
            img_type = imghdr.what(path)
        except Exception, e:
            img_type = None
        try:
            img_type_cache = imghdr.what(img_cache)
        except Exception, e:
            img_type_cache = None
        # check if there is a cached file, if yes we can skipp nearly everything
        # skip directly if it is a a gif image
        # and we're not doing a thumbnail
        # try to generate even if exists in case we couldn't determine the file type (broken file)
        if (not os.path.isfile(img_cache) or not img_type_cache) and (img_type != 'gif' or square):
            exif = None
            try:
                img_src = Image.open(path)
            except Exception, e:
                return (None, None)

            # try to preserve exif information so that loading these can be later
            # done from all filesizes (should decrease loading times)
            # If there is no exif information we silence the error
            try:
                if exif_rotate and hasattr(img_src, '_getexif'): # only present in JPEGs
                    for orientation in ExifTags.TAGS.keys():
                        if ExifTags.TAGS[orientation]=='Orientation':
                            break
                    exif = img_src._getexif()       # returns None if no EXIF data
                    if exif:
                        exif = dict(exif.items())
                        orientation = exif[orientation]

                        if orientation == 3:   img_src = img_src.transpose(Image.ROTATE_180)
                        elif orientation == 6: img_src = img_src.transpose(Image.ROTATE_270)
                        elif orientation == 8: img_src = img_src.transpose(Image.ROTATE_90)
            except Exception, e:
                # Pass errors during exif rotation
                # Nice to have but not necessary
                pass

            if square:
                img_out = ImageOps.fit(img_src, (width, height), Image.ANTIALIAS)
            else:
                img_src.thumbnail((width,height), Image.ANTIALIAS)
                img_out = img_src

            # caching
            try:
                img_out.save(img_cache, img_type, quality=quality)
            except Exception, e:
                raise e


        # either we had a cached image or the work is done, so read the
        # thumb for the correct filetype and return everything
        if img_type != 'gif' or square:
            file_to_return = img_cache
        else:
            file_to_return = path

        with open(file_to_return, 'rb') as image:
            return (image.read(), img_type)

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

        with open(absimagepath, 'rb') as image:
            response.content_type = 'image/%s' % imghdr.what(absimagepath)
            return image.read()
        return None
