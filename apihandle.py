from urllib import request, parse
from collections import namedtuple
from xml.etree import ElementTree
from xml.parsers import expat
import json

# TODO: Add key verification
# TODO: Add multi-query request (urllib.parse.encode)


class RequestAPI(object):
    """Handles links, parameters and connections to source API"""

    def __init__(self, api, **kwargs):
        self.api = api
        self.pars = kwargs
        self.url = self.build_link()
        self.resp = self.get_resp()

    def build_link(self):
        """Returns full url to connect and get data"""

        api_scheme, api_netloc, api_path, api_query, api_fragment = parse.urlsplit(self.api)

        Link = namedtuple('Link', 'scheme, netloc, path, query, fragment')
        url_pars = Link(scheme=api_scheme,
                        netloc=api_netloc,
                        path=api_path,
                        query=api_query,
                        fragment=api_fragment)

        url = url_pars._replace(**self.pars)

        return parse.urlunsplit(url)

    def get_resp(self):
        """Connects and pulls xml data"""

        data = request.urlopen(self.url)
        enc = data.headers.get_content_charset()

        return data.read().decode(enc)


class ParseAPI(RequestAPI):
    """Parsing any API response"""

    def __init__(self, api, **kwargs):
        super().__init__(api, **kwargs)

        if self.resp[0] == '<':
            self.root = self.parse_xml()
        else:
            self.root = self.parse_json()

    def parse_xml(self):
        """Parses xml objects"""

        return ElementTree.fromstring(self.resp)

    def parse_json(self):
        """Parses json objects"""

        return self.resp


# source_api = 'https://jsonplaceholder.typicode.com/comments'
source_api = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req=02/03/2002'
par = 'date_req'
value = '16/05/2020'

pars = {
    'query': f'{par}={value}'
}

my_req = ParseAPI(source_api, **pars)
# my_req = ParseAPI(source_api)

# For XML data type processing

print(my_req.root.tag, my_req.root.attrib)

for child in my_req.root:
    currency = child.find('CharCode').text
    value = child.find('Value').text
    print(f'{currency}: {value}')
    print('-' * 20)

# For JSON data processing
# print(my_req.root)
