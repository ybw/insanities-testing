# -*- coding: utf-8 -*-
import os

from insanities.forms import *
from insanities.forms import widgets
from insanities.ext.filefields import FileFieldSet, FileFieldSetConv, \
                                      UploadedFile

import cfg


class MyUploadedFile(UploadedFile):

    temp_path = os.path.join(cfg.MEDIA, 'temp')
    temp_url = '/media/temp/'


class FileForm(Form):

    fields = [
        Field('accept', label='I accept the terms of service',
              conv=convs.Bool(required=True),
              widget=widgets.CheckBox()),
        FileFieldSet('file', label='File',
                     file_cls=MyUploadedFile,
                     conv=FileFieldSetConv(required=True),
                     template='fileinput.html'),
    ]


class SimpleFileForm(Form):
    template='forms/paragraph.html'

    fields = [
        FileField('file', label='File',
                  conv=convs.SimpleFile(),
                  widget=widgets.Widget(template='fileinput.html')),
    ]

