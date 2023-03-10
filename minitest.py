import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom


doc1 = ET.parse(sys.argv[1])
doc2 = ET.parse(sys.argv[2])

root1 = doc1.getroot()
root2 = doc2.getroot()
