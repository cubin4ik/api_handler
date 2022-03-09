# Module to quickly fetch API data from any source given
# using just a link provided and parameters

from urllib import request, parse
from collections import namedtuple
from datetime import datetime
from xml.etree import ElementTree
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
    """Parsing any API response using parent module to fetch data silently"""

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

        return json.loads(self.resp)


def example():
    """Example of usage"""

    source_api = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req=02/03/2002'
    par_name = 'date_req'
    par_value = datetime.today().strftime('%d/%m/%Y')

    pars = {'query': f'{par_name}={par_value}'}
    my_req = ParseAPI(source_api, **pars)  # a single line to get data from API

    # For XML data type processing
    print(my_req.root.tag, my_req.root.attrib)
    for child in my_req.root:
        currency = child.find('CharCode').text
        par_value = child.find('Value').text
        print(f'{currency}: {par_value}')
        print('-' * 20)

    # For JSON data type processing use the code below
    # for data in my_req.root:
    #     print(data['postId'])


if __name__ == '__main__':
    example()
