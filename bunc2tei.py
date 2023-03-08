import os
import xml.etree.ElementTree as ET

path = 'home/spassova/BGCorpusExamples'
files = os.listdir(path)

tree = ET.parse(path + '/' + files[0])
root = tree.getroot()



