# -*- coding: utf-8 -*-
from tornado.web import RequestHandler

DEFAULT_RESPONSE = 'Tornado image processing server'


class MainHandler(RequestHandler):
    """
    Default page handler
    """

    def initialize(self, default_page=None, params=None):
        self._template = default_page
        self._params = params

    def get(self):
        """
        Root page handler can render template
        """
        if self._template and self._params:
            self.render(self._template, params=self._params)
        else:
            self.write(DEFAULT_RESPONSE)


class Action(object):
    """
    Image processing action description
    """
    def __init__(self, name):
        """
        Name - wrapped processing function name
        Options - *args
        """
        self.__name = name
        self.__options = []

    def add_option(self, option):
        """
        Append arg to action
        """
        self.__options.append(option)

    def get_options(self):
        return self.__options

    @property
    def name(self):
        return self.__name