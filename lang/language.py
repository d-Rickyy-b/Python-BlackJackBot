# -*- coding: utf-8 -*-

import codecs
import configparser
import os

__author__ = 'Rico'
dir_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir_path, "translations.ini")

translations = configparser.ConfigParser()
translations.read_file(codecs.open(file_path, encoding="UTF-8"))


# translate returns the translation for a specific string
def translate(string: str, language: str) -> str:
    """Returns the translation in a specific language for a specific string"""
    if language in translations and string in translations[language]:
        return translations[language][string]
    elif language == "br":
        return translations["pt_BR"][string]
    elif "en" in translations and string in translations["en"]:
        return translations["en"][string]
    return string


def translate_all(string: str) -> set:
    """Returns all the translations of a specific string"""
    strings = []
    lang_list = ["de", "en", "nl", "eo", "br", "es", "ru", "fa"]

    for lang in lang_list:
        strings.append(translate(string, lang))

    return set(strings)
