import re
import sys
import xml.etree.ElementTree as ET

def escape(file):        
    with open(sys.argv[i], "r+") as f:
        print("opened")
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




#for i in range(1, len(sys.argv)):
#    try:
#        ET.parse(sys.argv[i])
#        print("parsed")
#    except:
#        print("not parsed")
#        replace(sys.argv[i])
        

