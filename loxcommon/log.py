import logging
from os.path import exists
from logging import Formatter
from logging import StreamHandler
from logging import getLogger
from logging.handlers import TimedRotatingFileHandler
from sys import stdout

try:
    from ConfigParser import ConfigParser, DEFAULTSECT
    from ConfigParser import NoOptionError
    from ConfigParser import NoSectionError
    from urllib2 import URLError
except ImportError:
    from configparser import ConfigParser  # pylint: disable=F0401,W0611
    from configparser import NoOptionError  # pylint: disable=F0401,W0611
    from configparser import NoSectionError  # pylint: disable=F0401,W0611
    from urllib.error import URLError  # pylint: disable=F0401,W0611,E0611

DEFAULT_FORMATTER_STR = "%(asctime)s %(module)20s %(lineno)6s %(threadName)20s %(levelname)10s %(message)s"

loggers = dict()

def prepare_logging(configparser, log_path=None, log_name=None, log_level=logging.NOTSET):
    """
    sets up the root logger, Stream/File handlers, log format and log level
    """

    if not configparser or not isinstance(configparser, ConfigParser):
        configparser_tmp = ConfigParser()
        if type(configparser) == str:
            configparser_tmp.read(configparser)
        configparser = configparser_tmp

    # setup handlers
    handlers = []

    try:
        console = configparser.getboolean('logging', 'console')
        if console:
            handlers.append(StreamHandler(stdout))
    except NoSectionError:
        try:
            console = configparser.getboolean(DEFAULTSECT, 'console')
            if console:
                handlers.append(StreamHandler(stdout))
        except (NoSectionError, NoOptionError) as ex:
            handlers.append(StreamHandler(stdout))

    try:
        log_path_ini = configparser.get('logging', 'logfile')
        handlers.append(TimedRotatingFileHandler(log_path_ini, when='midnight', backupCount=30))
    except (NoSectionError, NoOptionError) as ex:
        if log_path and exists(log_path):
            handlers.append(TimedRotatingFileHandler(log_path, when='midnight', backupCount=30))

    # read log levels config
    try:
        log_format = configparser.get('logging', 'format', raw=True)
        if log_format:
            add_handlers(log_name, handlers, log_format)
        else:
            add_handlers(log_name, handlers, DEFAULT_FORMATTER_STR)
    except (NoSectionError, NoOptionError) as ex:
        add_handlers(log_name, handlers, DEFAULT_FORMATTER_STR)

    # read log levels config
    try:
        for (name, value) in configparser.items('loglevels'):
            getLogger(__name__).info("Setting logger %s to %s", name, value)
            logger = getLogger(name)

            if value not in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']:
                getLogger(__name__).error("unrecognised loglevel %s for logger %s, skipping", value, name)
                continue

            value = eval('logging.%s' % value)
            logger.setLevel(value)
    except NoSectionError:
        logger = getLogger(log_name)
        logger.setLevel(log_level)


def add_handlers(log_name, handlers, formatter_str):
    logger = getLogger(log_name)
    for handler in handlers:
        handler.setFormatter(Formatter(formatter_str))
        logger.addHandler(handler)
