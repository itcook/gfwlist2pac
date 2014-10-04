import re

with open('1000.log', 'rb') as f:
    for line in f:
        line = line.strip()
        m = re.findall('connecting (.*?):', line)
        if m:
            print m[0]
