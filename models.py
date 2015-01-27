#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from couchdb.mapping import Document, TextField, IntegerField, DateTimeField

class Paste(Document):
    _id = TextField()
    content = TextField()
    filetype = TextField()
    registered = DateTimeField(default=datetime.now)
    site = TextField()
