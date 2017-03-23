# -*- coding: utf-8 -*-

import codecs
import configparser
import os

__author__ = 'Rico'

path = os.path.dirname(os.path.abspath(__file__))
translations = configparser.ConfigParser()
translations.read_file(codecs.open(path + "/translations.ini", "r", "UTF-8"))


# translate returns the translation for a specific string
def translate(string, language):
    if language in translations and string in translations[language]:
        return translations[language][string]
    elif language == "br":
        return translations["pt_BR"][string]
    elif "en" in translations and string in translations["en"]:
        return translations["en"][string]
    return string
