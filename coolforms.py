## 
## coolforms.py
## 
## Created by Frederic DELBOS - fred.delbos@gmail.com on Dec 13 2013.
## This file is subject to the terms and conditions defined in
## file 'LICENSE.txt', which is part of this source code package.
## 

import json


# CoolForms
# =========

# CoolForm is the main class where everything happend. Basically you instantiate it
# and then call it's methods to add pages, lines, fields, and validators. For
# example to create a form and print it's json output do:
#
# ```
# import coolforms
#
# myform = coolforms.CoolForm("myform", "/truc")
# myform.page("First Page", "this is my first page")
# myform.line()
# myform.field("first_name", "text", "First Name", 2)
# myform.field("last_name", "text", "Last Name", 2)
# myform.line()
# myform.field("email", "text", "Email", 2)
# myform.validator("email", "Invalid email address")
# print myform.dump(2)
# ```
#
# Also note that a call always return the newly created object. For example
# you could do that if you wish:
#
# ```
# ...
# fld = myform.field("email", "text", "Email", 2)
# fld.label = "Email Address"
# fld.validator("email", "Invalid email address")
# ...
# print myform.dump(2)
# ```
#
# For a depeer explenation on the form content please refere to the
# [Form Definition page](https://github.com/fdelbos/coolforms/wiki/Form-Definition)
# on the coolform wiki.
class CoolForm():

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

    class Page:
        def __init__(self, title=None, description=None):
            self.title = title
            self.description = description
            self.lines = []

        def line(self, *args, **kwargs):
            l = CoolForm.Line(*args, **kwargs)
            self.lines.append(l)
            return l


    class Line:
        def __init__(self):
            self.fields = []
        
        def field(self, *args, **kwargs):
            f = CoolForm.Field(*args, **kwargs)
            self.fields.append(f)
            return f


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


    class Validator:
        def __init__(self, name, message=None, options={}):
            self.name = name
            self.message = message
            self.options = options


    # ### dump(indent=None)
    # Returns a JSON string representing the form
    def dump(self, indent=None):
        return json.dumps({'form': self}, cls=CoolForm.__Encoder__, indent=indent)

    class __Encoder__(json.JSONEncoder):
        def default(self, obj):
            return obj.__dict__
