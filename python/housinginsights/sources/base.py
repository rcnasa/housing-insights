"""
Base Api Connection classes.
"""

from urllib.parse import urljoin

from housinginsights.config.base import HousingInsightsConfig

import requests


class BaseApiConn(object):
    """
    Base API Connection to inherit from. Proxy support is built in,
    because if you do enough scraping, I promise you you're gonna get
    your IP blocked at some point.
    """
    def __init__(self, baseurl, proxies=None):
        """
        :param baseurl: URL endpoint of the API.
        :type baseurl: String.

        :param proxies: Proxies to use for the connection (HTTP or socks5).
                        Example: {'http': 'socks5://user:pass@someip:port',
                                  'https': 'socks5://user:pass@someip:port'}
        :type  proxies: dict of String.
        """
        self.session = requests.Session()
        self.baseurl = baseurl
        self.proxies = proxies

    def get(self, urlpath, params=None, **kwargs):
        """
        Thin wrapper around requests.get() that adds in proxy value
        and relative url joining.

        :param urlpath: URL path to be joined to the baseurl.
                        Example: if baseurl is https://www.somesite.com/api,
                                 and urlpath is /v2, the end result
                                 is https://www.somesite.com/api/v2.
        :type  urlpath: String.

        :param params: Dictionary of request parameters.
        :type  params: dict of String.
        """
        if self.baseurl[-1] == '/':
            self.baseurl = self.baseurl[:-1]
        if urlpath[0] != '/':
            urlpath = '/' + urlpath
        url = self.baseurl + urlpath
        return self.session.get(url, params=params, proxies=self.proxies, **kwargs)

    def post(self, urlpath, data=None, **kwargs):
        """
        Thin wrapper around requests.post() that adds in proxy value
        and relative url joining.

        :param urlpath: URL path to be joined to the baseurl.
                        Example: if baseurl is https://www.somesite.com/api,
                                 and urlpath is /v2, the end result
                                 is https://www.somesite.com/api/v2.
        :type  urlpath: String.

        :param params: Dictionary of request parameters.
        :type  params: dict of String.
        """
        url = urljoin(self.baseurl, urlpath)
        return self.session.post(url, data=data, proxies=self.proxies, **kwargs)


class BaseApiManager(object):

    classname = "base"

    def __init__(self, config_file):
        self.config = self.get_config(config_file)

    def get_config(self, config_file):
        config = HousingInsightsConfig(config_file)
        return config.get_section(self.__class__.classname)

