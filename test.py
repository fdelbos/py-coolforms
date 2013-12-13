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

    def test_make_form(self):
        f = cf.CoolForm("form", "/truc")
        f.page("First Page", "this is my first page")
        f.line()
        f.field("f1", "text", "a text field", 1, "some help")
        f.field("f2", "text", "a text field", 1, "some help")
        f.line()
        f.field("email", "text", "an email field", 1)
        f.validator("email", "invalid email")
        print f.dump(2)


if __name__ == '__main__':
    unittest.main()
