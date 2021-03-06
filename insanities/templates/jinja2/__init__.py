# -*- coding: utf-8 -*-

from os.path import dirname, abspath, join
import logging
logger = logging.getLogger(__name__)

import jinja2
from jinja2.utils import Markup
__all__ = ('TemplateEngine', 'TEMPLATE_DIR')

CURDIR = dirname(abspath(__file__))
TEMPLATE_DIR = join(CURDIR, 'templates')


class TemplateEngine(object):
    def __init__(self, paths, cache = False, autoescape = True):
        '''
        paths - list of paths
        '''
        self.env = jinja2.Environment(
            loader = jinja2.FileSystemLoader(paths),
            autoescape = autoescape,
            extensions=['jinja2.ext.with_'],
        )

    def render(self, template_name, **kw):
        'Interface method'
        return Markup(self.env.get_template(template_name).render(**kw))
