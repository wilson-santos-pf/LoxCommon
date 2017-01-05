"""
Module holding configuration and configparser related functions
"""

from logging import getLogger
from logging import StreamHandler
import os
from os.path import exists

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


class ConfigSingleton(object):
    """
    Singleton which has all configuration related info.
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, module, ini_file=None, defaults=None):
        if not hasattr(self, 'config_parser'):
            self.config_parser = ConfigParser(defaults=defaults)
            if module:
                self.module = module
            if not ini_file:
                # not using config_parser.read([f1, f2, ...]) because it reads every file in the list, silently
                #  overriding the options. The approach below allows us to know which file is being used
                files = ['{}.ini', os.path.expanduser('~/.config/{}/config.ini'), os.path.expanduser('~/{}.ini'),
                         '/etc/{}.ini']

                for f in files:
                    f = f.format(module)
                    if exists(f):
                        self.ini_file = f
                        break
            else:
                self.ini_file = ini_file

            print(self.__class__.__name__ + ' reading ini file: ' + self.ini_file)
            self.config_parser.read(self.ini_file)

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
            result = self.config_parser.get(section, field, raw=raw, vars=vars)
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
            result = self.config_parser.getboolean(section, field)
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
            result = self.config_parser.getint(section, field)
        except (NoOptionError, NoSectionError):
            result = default
        return result
