"""
This module is made to automatically return ILR scores of strings/files.
"""

__version__ = '1.0'
__author__ = 'Brandon Swenson'
__contact__ = 'bmswens@gmail.com'

import requests
import argparse

URL = "https://auto-ilr.ll.mit.edu/instant/summary3"

SUPPORTED_LANGUAGES = [
    "Arabic",
    "Chinese-Simplified",
    "Chinese-Traditional",
    "Croatian",
    "Dari",
    "English",
    "Farsi",
    "French",
    "German",
    "Korean",
    "Central Kurdish (Sorani)",
    "Pashto",
    "Portuguese",
    "Russian",
    "Serbian",
    "Spanish",
    "Tagalog",
    "Turkish",
    "Urdu",
]


class LanguageNotSupportedError(Exception):
    """
    Raised when the chosen language is supported.
    """
    pass


def get_level(content, language):
    """
    Returns an integer with the ILR level of the content provided, utilizing MIT's auto-ilr website.
    :param content: string object that contains the text to be assigned a level.
    :param language: string object with the name of the language of the content.
    :return: an integer with the score of the content.
    """

    if language not in SUPPORTED_LANGUAGES:
        raise LanguageNotSupportedError("{} is not a supported language.".format(language))

    if len(content) < 75 or len(content) > 70000:
        raise ValueError("AutoILR can only estimate level on text between 75 and 70000 characters long.")

    ilr_level = 0

    payload = {
        "Language": language,
        "Text": content
    }

    response = requests.post(URL,
                             data=payload)

    if not response.ok:
        raise ConnectionError("A proper connection to {} could not be established.".format(URL))

    for line in response.text.split('\n'):

        if line.lower().count("estimated ilr level:"):

            try:

                ilr_level = int(line[line.find(":") + 2: line.find(":") + 3])

            except ValueError:

                raise Exception("Could not parse ILR level line.")

    return ilr_level


def get_levels(content, language=None):
    """
    Returns a list of integers whose value is for the content of the same index.
    :param content: Either a list of strings, or a list of dictionaries that contain 'content' and 'language' keys.
    :param language: Optional, only needed if only passing in a list of strings for 'content'.
    :return: A list of integers whose value corresponds to the content in the same index.
    """

    if type(content) != list:

        raise TypeError("'content' parameter needs to be either a list of strings, or a list of dicts.")

    # if a language is supplied, assume it applies to all items in a list
    if language:

        return [get_level(string, language) for string in content]

    # otherwise, it should be a list of dict with 'language' and 'content' keys
    else:

        return [get_level(d.get('content'), d.get('language')) for d in content]


if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog="AutoILR",
                                     description="Used to get the ILR level of some content.",
                                     epilog="For help, or to report bugs, please contact bmswens@gmail.com",
                                     usage="AutoILR [-h] [-f] language content",
                                     )

    parser.add_argument("language",
                        nargs=1,
                        type=str,
                        help="The target language of the content provided.",
                        choices=SUPPORTED_LANGUAGES
                        )

    parser.add_argument('content',
                        metavar="content",
                        type=str,
                        nargs=argparse.REMAINDER,
                        help='The content to be analyzed.',
                        )

    parser.add_argument(*['--file', '-f'],
                        action='store_true',
                        dest='file',
                        default=False,
                        help="Use if you're passing in text files that need to be read, instead of the content itself.",
                        )

    args = parser.parse_args()

    arg_language = args.language[0]

    if args.file:

        arg_content = []

        for f in args.content:

            with open(f, 'r') as in_file:

                text = ''.join(in_file.readlines())

                arg_content.append(text)

    else:

        arg_content = args.content

    for item in arg_content:

        print(get_level(item, arg_language))
