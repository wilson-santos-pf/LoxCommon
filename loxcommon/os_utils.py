"""
Module with some file handling utilities.
"""
import os
import subprocess
import psutil
import getpass
import sys
from logging import getLogger


def mkdir_p(path):
    """
    Similar to mkdir -p
    :param path:
    :return:
    """

    if os.path.exists(path):
        return

    par = os.path.split(path)[0]
    if os.path.exists(par):
        os.mkdir(path)
        getLogger(__name__).debug('created directory: %s' % path)
    else:
        mkdir_p(par)
        os.mkdir(path)


def remove_extension(path, extension):
    import re
    return re.sub(extension + '$', '', path)


FILE_ATTRIBUTE_HIDDEN = 0x02
FILE_ATTRIBUTE_NORMAL = 0x80


def open_file_ext(url):
    if sys.platform == 'win32':
        p = os.startfile(url)
    elif sys.platform == 'darwin':
        p = subprocess.Popen(['open', url])
    else:
        try:
            p = subprocess.Popen(['xdg-open', url])
            p.communicate()
        except OSError as ex:
            getLogger(__name__).exception('Unable to open %s' % url, ex)


def change_file_attribute(filename, attr_flag):
    if sys.platform == 'win32':
        import ctypes
        try:
            eval('unicode(filename)')
            u_filename = unicode(filename)
        except SyntaxError:
            u_filename = str(filename)

        ret = ctypes.windll.kernel32.SetFileAttributesW(u_filename, attr_flag)
        if not ret:
            getLogger(__name__).error('cannot change file %s attributes to %s' % (u_filename, attr_flag))


def hide_file(filename):
    change_file_attribute(filename, FILE_ATTRIBUTE_HIDDEN)


def unhide_file(filename):
    change_file_attribute(filename, FILE_ATTRIBUTE_NORMAL)


def get_keys_path(localbox_path):
    """
    Get the keys location for this localbox path.

    >>> get_keys_path('/a/b/c')
    'a'
    >>> get_keys_path('a')
    'a'
    >>> get_keys_path('/a/b/c/')
    'a'
    >>> get_keys_path('a/b')
    'a'

    :param localbox_path:
    :return: it returns the parent 'directory'
    """
    if localbox_path.startswith('/'):
        localbox_path = localbox_path[1:]

    keys_path = localbox_path.split('/')[0]

    getLogger(__name__).debug('keys_path for localbox_path "%s" is "%s"' % (localbox_path, keys_path))
    return keys_path


def find_pid_for_file(filesystem_path):
    """
    Get the process id of the process that has the file opened.

    :param filesystem_path:
    :return:
    """
    # FIXME: This does not work 100% of the time
    for proc in psutil.process_iter():
        pinfo = proc.as_dict(attrs=['pid', 'username', 'open_files'])
        if pinfo['username'] == getpass.getuser():
            if pinfo['open_files'] is not None:
                for of in pinfo['open_files']:
                    if filesystem_path in of.path:
                        return pinfo['pid']


if __name__ == "__main__":
    # python os_utils.py -v
    import doctest

    doctest.testmod()
