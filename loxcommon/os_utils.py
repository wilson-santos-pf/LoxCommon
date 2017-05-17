"""
Module with some file handling utilities.
"""
import getpass
import hashlib
import os
import subprocess
import sys
from base64 import b64encode
from logging import getLogger
from os.path import isdir
from shutil import rmtree

try:
    from urllib import quote_plus
    from urllib import unquote_plus
except:
    from urllib.parse import quote_plus
    from urllib.parse import unquote_plus

import psutil


def remove_extension(path, extension):
    import re
    return re.sub(extension + '$', '', path)


FILE_ATTRIBUTE_HIDDEN = 0x02
FILE_ATTRIBUTE_NORMAL = 0x80


def is_windows():
    return os.name == 'nt'


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


def shred(filesystem_path):
    """
    Remove a file/directory permanently.

    :param filesystem_path:
    :return: True is success, False otherwise.
    """
    # TODO: for now this provides only an "interface" and uses the common removal functions.
    # latter on this will be replace by an library/function/algorithm/ that removes the files without the possibility
    # of recovery.
    try:
        if isdir(filesystem_path):
            rmtree(filesystem_path)
        else:
            os.remove(filesystem_path)

        return True
    except OSError as ex:
        getLogger(__name__).exception(ex)
        return False


def hash_file(filesystem_path):
    with open(filesystem_path, 'rb') as infile:
        contents = infile.read()
        m = hashlib.md5()
        m.update(contents)
        result = b64encode(m.digest())
        getLogger(__name__).debug('hash for %s is %s' % (filesystem_path, result))
        return result


def get_path_for_url(path):
    """
    Receives a LocalBox path and returns it ready to be used on a HTTP request.

    :param path: LocalBox path (eg,
    :return:
    """
    return quote_plus(path.encode('utf8')).strip('/')


def get_path_from_url(path):
    """
    Do the reverse operation of get_path_for_url
    :param path:
    :return:
    """
    return unquote_plus(path.decode('utf8'))


if __name__ == "__main__":
    # python os_utils.py -v
    import doctest

    doctest.testmod()
