import collections
import hashlib
import logging
from typing import Optional
from urllib.parse import urljoin

import requests
import xmltodict as xmltodict

import settings


class Client:
    def __init__(self, base_url: str, secret: str):
        self.base_url = base_url
        self.secret = secret


def api_get_call(endpoint: str, client: Client) -> Optional[collections.OrderedDict]:
    """
    TODO - add param option
    """

    plaintext = endpoint + client.secret
    sha1 = hashlib.sha1()
    sha1.update(plaintext.encode('utf-8'))
    checksum = sha1.hexdigest()

    url = urljoin(client.base_url, endpoint + "?checksum=" + checksum)

    try:
        r = requests.get(url)
    except Exception as e:
        logging.error("Failed to perform API call")
        logging.error(e)
        return None

    if int(r.status_code / 100) != 2:
        logging.error("Non 2xx HTTP status code response")
        logging.error(r.text)
        return None

    if settings.DEBUG:
        print(r.text)

    return xmltodict.parse(r.text)


def getMeetings(client: Client) -> Optional[collections.OrderedDict]:
    return api_get_call("getMeetings", client)

