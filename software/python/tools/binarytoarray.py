#!/usr/bin/env python

import sys


f = open(sys.argv[1],"rb")
b = f.read()
f.close()
b = list(b)
b = map(ord,b)
b = map(hex,b)
print(",".join(b))
