# coding=utf-8
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

import sys
import json
import codecs
import glob

f = codecs.open(sys.argv[2], 'w', "utf-8")
items = []
files = glob.glob(sys.argv[1]+"/*.gbib")
for file in files:
    bib = codecs.open(file, 'r', "utf-8")
    data = json.load(bib)
    items.extend(data)

f.write(json.dumps(items))
f.close()

