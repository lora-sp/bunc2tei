import os
import xml.etree.ElementTree as ET

path = '/home/spassova/BGCorpusExamples'
files = os.listdir(path)

tree = ET.parse(path + '/' + files[0])
root = tree.getroot()

titles = root.findall('.//*[@type='title']')
domains = root.findall('.//*[@type='domain']')
pageURLs = root.findall('.//*[@type='pageURL']')
ids = root.findall('.//*[@type='id']')
mainImageURLs = root.findall('.//*[@type='mainImageURL']')
mainImageTexts = root.findall('.//*[@type='mainImageTexts']')
mainImageSources = root.findall('.//*[@type='mainImageSources']')
authors = root.findall('.//*[@type='authors']')
authorURLs = root.findall('.//*[@type='authorURLs']')
categories = root.findall('.//*[@type='category']')
subCategories = root.findall('.//*[@type='subCategory']')
tags = root.findall('.//*[@type='tags']')
datesPublished = root.findall('.//*[@type='datePublished']')
timesPublished = root.findall('.//*[@type='timePubished']')
datesModified = root.findall('.//*[@type='dateModified']')
timesModified = root.findall('.//*[@type='timeModified']')

number_of_texts = len(root.findall('{http://www.tei-c.org/ns/1.0}text'))

for elem in root.findall('*'):
    root.remove(elem)

root.tag = 'teiCorpus'

for i in range(number_of_texts):
    tei = ET.SubElement(root, 'TEI')
    teiHeader = ET.SubElement(tei, 'teiHeader')
    fileDesc = ET.SubElement(teiHeader, 'fileDesc')
    titleStmt = ET.SubElement(fileDesc, 'titleStmt')
    textSigle = ET.SubElement(titleStmt, 'textSigle')
    textSigle.text = 'BNC/TST.' + f'{i:05}'
    sourceDesc = ET.SubElement(fileDesc, 'sourceDesc')
    


    




ET.indent(tree, '  ')
ET.register_namespace('', 'http://www.tei-c.org/ns/1.0')
tree.write('04_output.xml', encoding='utf-8', xml_declaration=True, method='xml', short_empty_elements=True)