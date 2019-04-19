#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 10:52:26 2019

@author: user
"""

url_string1 = "https://classes.berkeley.edu/search/class/?f%5B0%5D=sm_instructors%3A"
#Alexandre%20M.%20Bayen
url_string2 = "&f%5B1%5D=im_field_term_name%"
#3A851
url_string3 = "&f%5B2%5D=ts_course_level%3"
#Agrad


url = "{0}{1}{2}{3}{4}{5}".format(url_string1, "Alexandre%20M.%20Bayen", \
    url_string2, "3A851", url_string3, "Agrad")
print(url)