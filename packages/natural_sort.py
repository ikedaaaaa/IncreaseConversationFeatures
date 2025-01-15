#!usr/bin/env python
# -*- cording: utf-8 -*-

import re

def natural_sort(l):
    return sorted(l, key=natural_keys)

def to_int(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ to_int(c) for c in re.split(r'(\d+)', text) ]