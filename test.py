# 
# test.py
# 
# Created by Frederic DELBOS - fred.delbos@gmail.com on Dec 13 2013.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
# 

import unittest
import coolforms as cf

class TestSequenceFunctions(unittest.TestCase):

    def test_make_complex(self):
        f = cf.CoolForm("form", "/truc", submit="Submit", reset="Reset")
        f.customDirective("demo", "demo-directive")
        f.page("First Page", "this is my first page")
        f.line()
        f.field("passwd", "text", "passwd", mandatory=True, help="whatever...", options={"type":"password"})
        f.field("email", "text", "email", help="email").validator("email", "not an email")
        f.field("f1", "text", "show", help="type \"show\"").validator("min_size", "too small", options={'size':4})
        f.field("f2", "text", "hidden").showOn("f1", ["show"])
        f.customValidator("demo", "DemoModule", "demoFactory")
        f.page("Second Page", "this is the second page")
        f.line().field("f3", "text", "show 3", help="type \"show\"")
        f.line().field("redemo", "demo", "ReDemo", help="min 4").validator("min_size", "too small", options={'size':4})
        f.line().showOn("f3", ["show"]).field("demo", "text", "Demo", help="write \"demo\"").validator("demo", "not demo")
        f.page("Third Page", "this is the second page").showOn("f3", ["show"])
        f.line().field("f5", "text", "show 5", help="type \"show\"")
        print f.dump(2)

    def test_form_with_headers_and_hidden_values(self):
        f = cf.CoolForm("form", "", submit="Submit")
        f.hidden("test", 42).hidden("truc", "bidule").header("machin", "chose")
        f.page().line().field("toto", "text", "Toto")
        print f.dump()
        


if __name__ == '__main__':
    unittest.main()
