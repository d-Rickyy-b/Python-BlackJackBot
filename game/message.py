# -*- coding: utf-8 -*-

__author__ = 'Rico'

class Message(object):

    def __init__(self, message = ""):
        self.message = message

    def add_text(self, text):
        self.message += text

    def add_text_nl(self, text):
        self.message += "\n" + text

    def get_text(self):
        return self.message

    def __repr__(self):
        return self.message

    def __str__(self):
        return self.message