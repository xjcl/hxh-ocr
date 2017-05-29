
# usage:
# cat ~/Music/pics/hxh-textposts/*.txt | py3 all_ascii.py

import sys

for line in sys.stdin:
    for c in line:
        if ord(c) >= 128:
            print(c, line.rstrip())
