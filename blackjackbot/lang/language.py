# -*- coding: utf-8 -*-

import json
import os
import pathlib
import re
import logging

logger = logging.getLogger(__name__)

lang_path = pathlib.Path(__file__).parent.absolute()
maintainer_strings_path = lang_path / "strings"
custom_strings_path = lang_path / "custom_strings"

language_paths = [maintainer_strings_path, custom_strings_path]
languages = {}


class Translator(object):

    def __init__(self, lang_id):
        self.lang_id = lang_id or "en"

    def translate(self, string):
        return translate(string, self.lang_id)

    def __call__(self, string):
        """
        Wrapper for the translate method. Calling the object directly
        instead of the translate method will leave you with more tidy code
        """
        return self.translate(string)


def load_strings_from_dir(directory):
    """Reads the translation files into a dict. Overwrites the dict if already present"""
    with os.scandir(directory) as entries:
        for entry in entries:
            match = re.search(r"^translations_([a-z]{2}(-[a-z]{2})?)\.json$", entry.name)

            if not match:
                continue

            with open(entry.path, encoding="utf-8") as json_file:
                try:
                    data = json.load(json_file)
                except json.JSONDecodeError:
                    logger.error("Can't open translation file '{}'".format(entry.path))
                    continue

                file_lang_code = match.group(1)

                # Make sure the language file got a lang_code specified
                lang_code = data.get("lang_code", None)
                if not lang_code:
                    logger.error("No lang_code specified in translation file '{0}'".format(entry.path))
                    return

                if languages.get(lang_code, None):
                    logger.warning("Overwriting translations for lang_code: {0}".format(lang_code))

                logger.info("Loaded translation file {0} - language code: {1}".format(entry.name, lang_code))
                languages[lang_code] = data


def reload_strings():
    for path in language_paths:
        if not path.exists():
            logger.warning("The path for translations does not exist: {0}".format(path.name))
            continue
        load_strings_from_dir(path)

    if len(languages) == 0:
        logger.error("Coudln't load translations!")


def get_available_languages():
    """Return a list of available languages"""
    if len(languages) == 0:
        reload_strings()
    langs = []

    for key, value in languages.items():
        langs.append(get_language_info(key))

    return langs


def get_language_info(lang_code):
    """Returns information such as the lang_code, the language's name and the display name (with flag) for a certain language"""
    lang = get_language(lang_code)
    lang_name = lang.get("language_name", "N/A")
    lang_flag = lang.get("language_flag", "N/A")
    display_name = "{} {}".format(lang_name, lang_flag)

    return {"lang_code": lang.get("lang_code", "N/A"), "name": lang.get("language_name", "N/A"), "display_name": display_name}


def get_language(lang_code):
    """Returns the translation dict for a certain language if it exists. If not, return the English translations"""
    if len(languages) == 0:
        reload_strings()

    lang = languages.get(lang_code, None)
    if lang is None:
        if "-" in lang_code:
            return get_language(lang_code.split("-")[0])

        return languages["en"]
    return lang


def translate(string, lang_code="en"):
    """Returns the translation in a specific language for a specific string"""
    lang = get_language(lang_code)

    translated_string = lang.get(string, None)

    if translated_string is None:
        # We want to give at least an english string as a fallback if there is none available in the selected language

        if lang_code != "en":
            return translate(string, "en")
        logger.warning("Missing string '{}'!".format(string))
        return "STRING_NOT_AVAILABLE ('{}')".format(string)

    return translated_string
