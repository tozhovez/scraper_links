#from os import sys, path
import asyncio
import requests
import json
from pprint import pprint
#sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class LoaderError(Exception):
    """Class that encapsules errors returned by Loader."""

    @classmethod
    def from_dict(cls, dict_error):
        return cls(dict_error)

    def __init__(self, code):
        self.code = code

class LoaderContentTypeError(Exception):
    pass

class Loader:
    """Page loader."""

    async def fetch(self, url):
        with requests.get(url) as response:
            response.encoding = 'utf-8'
            if response.status_code == 200:
                if response.headers.get('content-type').lower() == "text/html; charset=utf-8":
                    return response.text
                else:
                  #print(response.headers.get('content-type'), url)
                  raise LoaderContentTypeError(response.headers.get('content-type'), url)
            else:
                error = response.status_code
                if error:
                    raise LoaderError.from_dict(error)
                raise LoaderError.from_dict(error)
