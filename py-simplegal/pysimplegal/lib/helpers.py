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


