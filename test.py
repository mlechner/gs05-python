#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Record import Record


# read example file
fname = "./example/output.txt"

with open(fname) as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

for i in content:
    myrecord = Record(i)
    for key in myrecord.data.keys():
        print(key, myrecord.data[key])