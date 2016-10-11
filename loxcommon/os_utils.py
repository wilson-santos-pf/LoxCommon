import logging
import os

import loxcommon.log as logging_utils


def mkdir_p(path):
    """
    Similar to mkdir -p
    :param path:
    :return:
    """

    print __name__
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


def getLogger():
    return logging_utils.loggers[__name__]
