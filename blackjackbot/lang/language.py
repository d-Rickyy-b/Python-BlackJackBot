# -*- coding: utf-8 -*-

import json
import os
import re

dir_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir_path, "strings")
languages = {}


def reload_strings():
    """Reads the translation files into a dict"""
    with os.scandir(file_path) as entries:
        for entry in entries:
            match = re.search(r"^translations_([a-z]+)\.json$", entry.name)

            if not match:
                continue

            with open(entry.path) as json_file:
                data = json.load(json_file)
                lang_code = match.group(1)
                languages[lang_code] = data


def get_available_languages():
    """Return a list of available languages"""
    langs = []

    for key, value in languages.items():
        lang_name = value.get("language_name", "N/A")
        lang_flag = value.get("language_flag", "N/A")
        display_name = "{} {}".format(lang_name, lang_flag)

        lang = {"lang_code": value.get("lang_code", "N/A"), "name": value.get("language_name", "N/A"), "display_name": display_name}
        langs.append(lang)

    return langs


def translate(string, lang_code="en"):
    """Returns the translation in a specific language for a specific string"""
    lang = languages.get(lang_code, None)

    if lang is None:
        if "_" in lang_code:
            return translate(string, lang_code.split("_")[0])

        lang = languages["en"]

    translated_string = lang.get(string, None)

    if translated_string is None:
        # We want to give at least an english string as a fallback if there is none available in the selected language

        if lang_code != "en":
            return translate(string, "en")
        return "STRING_NOT_AVAILABLE"

    return translated_string


reload_strings()
