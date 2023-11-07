import json
import sys

import requests
import unidecode


class UnicodeDecodeError(Exception):
    pass


def u2asc(input):
    """
    Converts/transliterates unicode characters to ASCII, using the unidecode package.
    Functionality is similar to the legacy code in adspy.Unicode, but may treat some characters differently
    (e.g. umlauts). Standard unidecode package only handles Latin-based characters.
    :param input: string to be transliterated. Can be either unicode or encoded in utf-8
    :return output: transliterated string, in either unicode or encoded (to match input)
    """

    # TODO If used on anything but author names, add special handling for math symbols and other special chars
    if sys.version_info < (3,):
        test_type = unicode
    else:
        test_type = str

    if not isinstance(input, test_type):
        try:
            input = input.decode("utf-8")
        except UnicodeDecodeError:
            raise UnicodeHandlerError("Input must be either unicode or encoded in utf8.")

    try:
        output = unidecode.unidecode(input)
    except UnicodeDecodeError:
        raise UnicodeHandlerError("Transliteration failed, check input.")

    if not isinstance(input, test_type):
        output = output.encode("utf-8")

    return output


def issn2info(token=None, url=None, issn=None, return_info="bibstem"):
    """
    Sends an ISSN to the JournalsDB API and returns the field specified by `return_info`
    Default info to be returned is bibstem
    """
    if issn and token and url:
        url_base = url + "/journals/issn/"
        request_url = url_base + issn
        token_dict = {"Authorization": "Bearer %s" % token}
        try:
            req = requests.get(request_url, headers=token_dict)
        except Exception as err:
            pass
        else:
            if req.status_code == 200:
                result = req.json()
                return result.get("issn", {}).get(return_info, None)
    return
