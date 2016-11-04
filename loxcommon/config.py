"""
Module holding configuration and configparser related functions
"""

from logging import getLogger
from logging import StreamHandler
import os

try:
    from ConfigParser import ConfigParser
    from ConfigParser import NoOptionError, NoSectionError
except ImportError:
    from configparser import ConfigParser  # pylint: disable=F0401
    # pylint: disable=F0401
    from configparser import NoOptionError, NoSectionError


def prepare_logger(name, loglevel=None, handlers=None):
    """
    Make sure the logging subsystem is initialized correctly
    """
    if handlers is None:
        handlers = [StreamHandler()]
    log = getLogger(name)
    log.setLevel(loglevel)
    for handler in handlers:
        log.addHandler(handler)


class ConfigSingleton(ConfigParser):
    """
    Singleton which has all configuration related info.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConfigSingleton, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    def __init__(self, module, location=None, defaults=None):
        ConfigParser.__init__(self, defaults=defaults)
        if not hasattr(self, 'configparser'):
            self.configparser = ConfigParser()
            if module:
                self.module = module
            if not location:
                self.configparser.read(['/etc/%s.ini' % module, os.path.expanduser('~/%s.ini' % module),
                                        os.path.expanduser('~/.config/%s/config.ini' % module),
                                        '%s.ini' % module])
            else:
                self.configparser.read(location)

    def get(self, section, field, raw=None, default=None, vars=None):
        """
        Returns the value of a certain field in a certain section on the
        configuration

        :param section: the [section] in which to look for the information
        :param field: the name of the configuration item to read
        :param default: Value to return when the config option can't be found
        :returns: the value of said configuration item
        """
        try:
            result = self.configparser.get(section, field, raw=raw, vars=vars)
        except (NoOptionError, NoSectionError):
            result = default
        return result

    def getboolean(self, section, field, default=None):
        """
        Returns the value of a certain field in a certain section on the
        configuration in a boolean context

        :param section: the [section] in which to look for the information
        :param field: the name of the configuration item to read
        :param default: Value to return when the config option can't be found
        :returns: the boolean value of said configuration item
        """
        try:
            result = self.configparser.getboolean(section, field)
        except (NoOptionError, NoSectionError):
            result = default
        return result

    def getint(self, section, field, default=None):
        """
        Returns the value of a certain field in a certain section on the
        configuration, cast to an int.

        :param section: the [section] in which to look for the information
        :param field: the name of the configuration item to read
        :returns: the integer value of said configuration item
        """
        try:
            result = self.configparser.getint(section, field)
        except (NoOptionError, NoSectionError):
            result = default
        return result
