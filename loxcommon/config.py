"""
Module holding configuration and configparser related functions
"""

import os
from os.path import exists

try:
    from ConfigParser import ConfigParser
    from ConfigParser import NoOptionError, NoSectionError
except ImportError:
    from configparser import ConfigParser  # pylint: disable=F0401
    # pylint: disable=F0401
    from configparser import NoOptionError, NoSectionError


class ConfigSingleton(ConfigParser):
    """
    Singleton which has all configuration related info.
    """

    def __init__(self, module, ini_file=None, defaults=None):
        ConfigParser.__init__(self, defaults=defaults)
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

        try:
            ConfigParser.read(self, self.ini_file)
        except AttributeError:
            raise Exception('No ini file found for module: %s' % module)

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
            result = ConfigParser.get(self, section, field, raw=raw, vars=vars)
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
            result = ConfigParser.getboolean(self, section, field)
        except (NoOptionError, NoSectionError):
            result = default
        return result

    def getint(self, section, field, default=None):
        """
        Returns the value of a certain field in a certain section on the
        configuration, cast to an int.

        :param section: the [section] in which to look for the information
        :param field: the name of the configuration item to read
        :param default: Value to return when the config option can't be found
        :returns: the integer value of said configuration item
        """
        try:
            result = int(ConfigParser.get(self, section, field))  # ConfigParser.getint does not work
        except (NoOptionError, NoSectionError):
            result = default
        return result
