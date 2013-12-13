## 
## coolforms.py
## 
## Created by Frederic DELBOS - fred.delbos@gmail.com on Dec 13 2013.
## This file is subject to the terms and conditions defined in
## file 'LICENSE.txt', which is part of this source code package.
## 

import json

class CoolForm():

    class __Encoder__(json.JSONEncoder):
        def default(self, obj):
            return obj.__dict__


    class Validator:
        def __init__(self, name, message=None, options={}):
            self.name = name
            self.message = message
            self.options = options


    class Field:
        def __init__(self, name, type, label=None, size=1, help=None):
            self.name = name
            self.type = type
            self.label = label
            self.size = size
            self.help = help
            self.validators = []

        def validator(self, *args, **kwargs):
            v = CoolForm.Validator(*args, **kwargs)
            self.validators.append(v)
            return v
            

    class Line:
        def __init__(self):
            self.fields = []
        
        def field(self, *args, **kwargs):
            f = CoolForm.Field(*args, **kwargs)
            self.fields.append(f)
            return f

    
    class Page:
        def __init__(self, title=None, description=None):
            self.title = title
            self.description = description
            self.lines = []

        def line(self, *args, **kwargs):
            l = CoolForm.Line(*args, **kwargs)
            self.lines.append(l)
            return l


    def __init__(self, 
                 name,
                 action,
                 method="POST", 
                 submit=None, 
                 reset=None):

        self.action = action
        self.name = name
        self.method = method
        self.submit = submit
        self.resest = reset
        self.pages = []

    def page(self, title=None, description=None):
        p = CoolForm.Page(title, description)
        self.pages.append(p)
        return p

    def line(self, *args, **kwargs):
        return self.pages[-1].line(*args, **kwargs)

    def field(self, *args, **kwargs):
        return self.pages[-1].lines[-1].field(*args, **kwargs)

    def validator(self, *args, **kwargs):
        return self.pages[-1].lines[-1].fields[-1].validator(*args, **kwargs)

    def json(self, indent=None):
        return json.dumps({'form': self}, cls=CoolForm.__Encoder__, indent=indent)
