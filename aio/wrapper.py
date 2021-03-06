import requests
from proxymanager import ProxyManager

class ApiWrapper(object):
    BASE_URL = None
    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    def __init__(self, proxy_file_path=None):
        self.__initialize_session()
        self.proxy_manager = ProxyManager(proxy_file_path)

    def __initialize_session(self):
        self.session = requests.session()
        self.session.headers.update(self.DEFAULT_HEADERS)

    def get_random_proxy(self):
        return self.proxy_manager.random_proxy().get_dict()

    def make_url(self, endpoint):
        is_full_url = endpoint.startswith('http')
        if not is_full_url and not self.BASE_URL:
            raise ValueError('Must set BASE_URL')
        return endpoint if is_full_url else self.BASE_URL + str(endpoint)

    def request(self, method, url, **kwargs):
        return self.session.request(method=method, url=self.make_url(url), proxies=self.get_random_proxy(), **kwargs)

    def get(self, url, **kwargs):
        return self.request('get', url, **kwargs)

    def post(self, url, **kwargs):
        return self.request('post', url, **kwargs)

    def put(self, url, **kwargs):
        return self.request('put', url, **kwargs)

    def patch(self, url, **kwargs):
        return self.request('patch', url, **kwargs)
