import sys
import xml.etree.ElementTree as ET
from lxml import etree
from io import StringIO

'''
for i in range(1, len(sys.argv)):
    print("file: " + str(i) + " " + sys.argv[i])
    try:
        ("normaler parse geklappt")
        parser = etree.XMLParser(recover=False)
        tree = ET.parse(sys.argv[i], parser)
        #tree = ET.parse(sys.argv[i])
        root = tree.getroot()
        print(root.tag)
    except:
        print("nö")
        #with open 
'''

parser = etree.XMLParser(recover=True)
tree = ET.parse("dnevnik.bg - 2020-01-02.xml", parser)
ET.register_namespace("", "http://www.tei-c.org/ns/1.0")
tree.write("outputTEST.xml", encoding='utf-8', xml_declaration=True, method='xml', short_empty_elements=True)


