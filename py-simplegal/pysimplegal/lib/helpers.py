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
        pass

    return (directories, files)

def get_file_type(path):
    import magic
    import re
    mime = magic.from_file(path)

    if re.search(r'directory', mime, re.IGNORECASE):
        filetype = 'directory'
    elif re.search(r'matroska', mime, re.IGNORECASE):
        filetype = 'video'
    elif re.search(r'JPEG|PNG|GIF', mime, re.IGNORECASE):
        filetype = 'image'
    else:
        filetype = 'unknown'

    return filetype
