from __future__ import \
    absolute_import  # to avoid: RuntimeWarning: Parent module 'test' not found while handling absolute import

import unittest
from os import remove

from loxcommon.config import ConfigSingleton


class TestConfig(unittest.TestCase):
    TMP_INI = '/tmp/test_conf.ini'

    def setUp(self):
        f = open(TestConfig.TMP_INI, 'w')
        s = ('[Flags]\n'
             'flag1 = True\n'
             'flag2 = 0\n'
             '[Numbers]\n'
             'int1 = 666\n')
        f.write(s)
        f.close()

    def tearDown(self):
        remove(TestConfig.TMP_INI)

    def test_getboolean(self):
        result = ConfigSingleton('test', TestConfig.TMP_INI).getboolean('Flags', 'flag1')
        self.assertTrue(type(result) == bool)
        self.assertTrue(result)

        result = ConfigSingleton('test', TestConfig.TMP_INI).getboolean('Flags', 'flag2')
        self.assertTrue(type(result) == bool)
        self.assertFalse(result)

    def test_getint(self):
        result = ConfigSingleton('test', TestConfig.TMP_INI).getboolean('Numbers', 'int1')
        self.assertTrue(type(result) == int)
        self.assertEquals(result, 666)


if __name__ == '__main__':
    unittest.main()
