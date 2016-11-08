"""
Module with some file handling utilities.
"""
import logging
import os
import subprocess
import sys
from logging import getLogger

import loxcommon.log as logging_utils


def mkdir_p(path):
    """
    Similar to mkdir -p
    :param path:
    :return:
    """

    if os.path.exists(path):
        getLogger().debug('%s already exists' % path)
        return

    par = os.path.split(path)[0]
    if os.path.exists(par):
        os.mkdir(path)
        getLogger().debug('mkdir: %s' % path)
    else:
        mkdir_p(par)
        getLogger().debug('mkdir: %s' % path)
        os.mkdir(path)


def remove_extension(path, extension):
    import re
    return re.sub(extension + '$', '', path)


def getLogger():
    try:
        return logging_utils.loggers[__name__]
    except KeyError:
        return logging.getLogger(__name__)


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
