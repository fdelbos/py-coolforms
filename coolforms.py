# ## Overview
#
# [py-coolform](https://github.com/fdelbos/py-coolforms)
# is a Form generator for [CoolForms](https://github.com/fdelbos/coolforms).
# Instantiate a CoolForm object and add pages, lines, fields, validators... Once you are done
# dump the form to JSON
# 
# Note that you have to call the methods in the right order:
#
# ```
# 1 page -> 2 line -> 3 field -> 4validator
# ```
#
# For example to create a form and print it's json output do:
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
# myform.page().line().field("name", "text").validator("email")
# ...
# print myform.dump(2)
# ```
#
# For a depeer explenation on the form content please refere to the
# [Form Definition page](https://github.com/fdelbos/coolforms/wiki/Form-Definition)
# on the coolform wiki.
import json

# ## API
#
#
# **CoolForm(name, action, method, submit, reset)**
#
# Constructor
#
# * **name** : Name of the form
# * **action** : URL to send data
# * **method** : HTTP method to use, default is POST
# * **submit** : Text to display on the submit button
# * **reset** : Text to display on the reset button, if not set, the button is not displayed
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
        self.reset = reset
        self.pages = []
        self.dependencies = []
        self.hiddens = {}
        self.headers = {}
        

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

    # Pages, Lines and Fields can be shown or hidden when a previously declared field  match a value.
    class Displayable:
        def __display__(self, display, field, *values):
            if hasattr(self, display) is False:
                self.__dict__[display] = {}
            if field not in self.__dict__[display]:
                self.__dict__[display][field] = []
            self.__dict__[display][field] += list(*values)
            return self

        # **showOn(field, *values)**
        #
        # Add a display constraint on a field. Elements are shown when some other field(s) match value(s).
        #
        # * **field** : Field to match
        # * **values** : A List of possible values
        def showOn(self, field, *values):
            return self.__display__('show_on', field, *values)

        # **hideOn(field, *values)**
        #
        # Add a display constraint on a field. Elements are hiddens when they match some other field(s) value(s).
        #
        # * **field** : Field to match
        # * **values** : A List of possible values
        def hideOn(self, field, *values):
            return self.__display__('hide_on', field, *values)

    # **page(title, description)**
    #
    # Add a page to the form.
    #
    # * **title** : Title for the page
    # * **description** : A description to be displayed
    class Page(Displayable):
        def __init__(self, title=None, description=None):
            self.title = title
            self.description = description
            self.lines = []

        def line(self, *args, **kwargs):
            l = CoolForm.Line(*args, **kwargs)
            self.lines.append(l)
            return l

    # **line()**
    #
    # Add a new line to the current page.
    class Line(Displayable):
        def __init__(self):
            self.fields = []
        
        def field(self, *args, **kwargs):
            f = CoolForm.Field(*args, **kwargs)
            self.fields.append(f)
            return f


    # **field(name, type, label, size, help, default)**
    #
    # Add a field to the current line.
    #
    # * **name** : Name for the field to be sent on submit
    # * **type** : Type of the field
    # * **size** : An integer
    # * **help** : Help to be displayed to the user
    # * **default** : Default value of the field
    # * **options** : Field specific options
    class Field(Displayable):
        def __init__(self,
                     name,
                     type,
                     label=None,
                     size=1,
                     help=None,
                     mandatory=False,
                     default=None,
                     options=None):
            self.name = name
            self.type = type
            self.label = label
            self.size = size
            self.help = help
            self.mandatory = mandatory
            self.default = default
            self.options = options
            self.validators = []

        def validator(self, *args, **kwargs):
            v = CoolForm.Validator(*args, **kwargs)
            self.validators.append(v)
            return v


    # **validator(name, message, options)**
    #
    # Add a validator to a field
    #
    # * **name** : Name of the validation function
    # * **message** : Message to be displayed in case of mismatch
    # * **options** : Some options to be passed to the validation function
    class Validator:
        def __init__(self, name, message=None, options={}):
            self.name = name
            self.message = message
            self.options = options

    # **customValidator(name, module, factory)**
    #
    # Enable the use of a custom validator. Must be called on a CoolForm object.
    #
    # * **name** : An alias for using the validator, that's how you call it in the form.
    # * **module** : AngularJS module where it is declared.
    # * **factory** : Factory function that returns the validator.
    def customValidator(self, name, module, factory):
        self.dependencies.append({
            'type':'validator',
            'name': name,
            'module': module,
            'factory': factory})
        return self

    # **customDirective(name, tag)**
    #
    # Enalble the use of a custom directive for a field. Must be called on a CoolForm object.
    #
    # * **name** : An alias inside the form.
    # * **tag** : The AngularJS tag to display the directive. Should be accessible from the forms's scope.
    def customDirective(self, name, tag):
        self.dependencies.append({
            'type':'directive',
            'name': name,
            'tag': tag})
        return self

    # **header(key, value)**
    #
    # Add a header to the ajax request
    #
    # * **key** : Name of the header
    # * **value** : Value of the header
    def header(self, key, value):
        self.headers[key] = value
        return self

    # **hidden(name, value)**
    #
    # Add an hidden field to be sent
    #
    # * **name** : Name of the field
    # * **value** : Value of the field
    def hidden(self, name, value):
        self.hiddens[name] = value        
        return self

    # **dump(indent=None)**
    #
    # Dumps the current state of the form to JSON. Must be called on a CoolForm object.
    #
    # * **indent** : An optionnal integer parameter that allows pretty printing.
    def dump(self, indent=None):
        return json.dumps({'form': self}, cls=CoolForm.__Encoder__, indent=indent)

    class __Encoder__(json.JSONEncoder):
        def default(self, obj):
            return {k: v for k, v in obj.__dict__.items() if v != None and v != [] and v != {}}
