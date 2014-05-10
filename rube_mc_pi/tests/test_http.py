"""Unit testing for the http plug in"""

import rube_mc_pi.http as http
from rube_mc_pi.http import HttpSource
import StringIO
import unittest


class TestHttp(unittest.TestCase): # pylint: disable=R0904
    """ All the unittests for the Http plugin
    """

    def test_http_plugin_source(self): # pylint: disable=C0111
        http_source = HttpSource({"address": "http://localhost/"})
        self.assertEquals("http://localhost/", http_source.address)
        http.urllib2.urlopen = mock_urlopen
        
        result = http_source.poll_state()
        self.assertEquals(result.id, 1)
        self.assertEquals(result.data, 2)
        
        

def mock_urlopen(url):  # pylint: disable=W0613
    """Used for monkey patch the URL openner 
    for the unit tests of http plugin"""
    return StringIO.StringIO("1,2")

