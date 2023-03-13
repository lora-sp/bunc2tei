import re
import sys
import xml.etree.ElementTree as ET

def escape(file):        
    with open(sys.argv[i], "r+") as f:
        file = f.read()
        file = re.sub('&(?!gt;|apos;|quot;|lt;|amp;)', '&amp', file)
        f.seek(0)
        f.write(file)
        f.truncate()

for i in range(1, len(sys.argv)):
    try:
        ET.parse(sys.argv[i])
    except: 
        escape(sys.argv[i])
        #ET.parse(sys.argv[i])
        #print("sucess")


