"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password

def get_thumb_filename(path):
    """ returns the thumbnail filename for a given picture
    """
    import md5

    md5sum = md5.new()
    md5sum.update(path)
    thumb_cache = "%s" % md5sum.hexdigest()

    return thumb_cache


def path_to_array(path):
    """ creates an incremental array from a path
        e.g:
            neon/file/folder/
            ['neon/', 'neon/file/', 'neon/file/folder']
    """
    folders = path.split("/")
    return folders


def get_folder_content(path):
    """ get content of a given directory split into files and folders
    """
    import os

    directories = []
    files = []
    try:
        for filename in os.listdir(path):
            absfilepath = "%s/%s" % (path, filename)
            if os.path.isdir(absfilepath):
                directories.append([filename, get_file_type(absfilepath)])
            else:
                files.append([filename, get_file_type(absfilepath)])
    except OSError, e:
        raise e

    directories.sort()
    files.sort()

    return (directories, files)

def get_file_type(path):
    import magic
    import re
    filetype = ''
    filegroup = ''

    mime = magic.from_file(path)
    print mime

    if re.search(r'directory', mime, re.IGNORECASE):
        mime = 'directory'
        filegroup = 'directory'
    elif re.search(r'MPEG v4', mime, re.IGNORECASE):
        mime = 'video/mp4'
        filegroup = 'video'
    elif re.search(r'WebM', mime, re.IGNORECASE):
        mime = 'video/webm'
        filegroup = 'video'
    elif re.search(r'matroska', mime, re.IGNORECASE):
        mime = 'video/x-matroska'
        filegroup = 'video'
    elif re.search(r'Apple QuickTime movie', mime, re.IGNORECASE):
        mime = 'video/quicktime'
        filegroup = 'video'
    elif re.search(r'JPEG|JPG|PNG|GIF|BMP', mime, re.IGNORECASE):
        mime = 'image'
        filegroup = 'image'
    else:
        mime = 'unknown'
        filegroup = 'unknown'

    return {'mime': mime, 'filegroup': filegroup}


def get_exif(path):
    from PIL import Image
    img = Image.open(path)
    return img._getexif()
