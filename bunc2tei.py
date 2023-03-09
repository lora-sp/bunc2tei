import os
import xml.etree.ElementTree as ET

path = "/home/spassova/BGCorpusExamples"
files = os.listdir(path)

tree = ET.parse(path + "/" + files[0])
root = tree.getroot()

titles = root.findall(".//*[@type='title']")
domains = root.findall(".//*[@type='domain']")
pageURLs = root.findall(".//*[@type='pageURL']")
ids = root.findall(".//*[@type='id']")
mainImageURLs = root.findall(".//*[@type='mainImageURL']")
mainImageTexts = root.findall(".//*[@type='mainImageTexts']")
mainImageSources = root.findall(".//*[@type='mainImageSources']")
authors = root.findall(".//*[@type='authors']")
authorURLs = root.findall(".//*[@type='authorURLs']")
categories = root.findall(".//*[@type='category']")
subCategories = root.findall(".//*[@type='subCategory']")
tags = root.findall(".//*[@type='tags']")
datesPublished = root.findall(".//*[@type='datePublished']")
timesPublished = root.findall(".//*[@type='timePublished']")
datesModified = root.findall(".//*[@type='dateModified']")
timesModified = root.findall(".//*[@type='timeModified']")
mainImageWidths = root.findall(".//*[@type='mainImageWidth']")
mainImageHeights = root.findall(".//*[@type='mainImageHeight']")
mainImageThumbnailURLs = root.findall(".//*[@type='mainImageThumbnailURL']")
texts = []

number_of_texts = 0
for text in root.iter("{http://www.tei-c.org/ns/1.0}text"):
    number_of_texts+=1
    for body in text:
        for div1 in body:
            for div2 in div1:
                for div3 in div2:
                    if div3.get('type') == "metadata":
                        div2.remove(div3)

                    texts.append(div2)
                    

#number_of_texts = len(root.findall("{http://www.tei-c.org/ns/1.0}text"))

for elem in root.findall("*"):
    root.remove(elem)

root.tag = "teiCorpus"

for i in range(number_of_texts):
    tei = ET.SubElement(root, "TEI")
    teiHeader = ET.SubElement(tei, "teiHeader")
    fileDesc = ET.SubElement(teiHeader, "fileDesc")
    titleStmt = ET.SubElement(fileDesc, "titleStmt")
    textSigle = ET.SubElement(titleStmt, "textSigle")
    textSigle.text = "BNC/TST." + f"{i:05}"
    sourceDesc = ET.SubElement(fileDesc, "sourceDesc")
    analytic = ET.SubElement(sourceDesc, "analytic")
    htitle = ET.SubElement(analytic, "h.title")
    htitle.text = titles[i].text
    hauthor = ET.SubElement(analytic, "h.author")
    hauthor.text = authors[i].text
    imprint = ET.SubElement(sourceDesc, "imprint")
    pubDateYear = ET.SubElement(imprint, "pubDate")
    pubDateYear.set("type", "year")
    pubDateYear.text = datesPublished[i].text[0:4]
    pubDateMonth = ET.SubElement(imprint, "pubDate")
    pubDateMonth.set("type", "month")
    pubDateMonth.text = datesPublished[i].text[5:7]
    pubDateDay = ET.SubElement(imprint, "pubDate")
    pubDateDay.set("type", "day")
    pubDateDay.text = datesPublished[i].text[8:10]
    pubDateTime = ET.SubElement(imprint, "pubDate")
    pubDateTime.set("type", "time")
    pubDateTime.text = timesPublished[i].text
    pubPlace = ET.SubElement(imprint, "pubPlace")
    ref = ET.SubElement(pubPlace, "ref")
    ref.set("type", "page_url")
    ref.set("target", pageURLs[i].text)





ET.indent(tree, "  ")
ET.register_namespace("", "http://www.tei-c.org/ns/1.0")
tree.write("04_output.xml", encoding="utf-8", xml_declaration=True, method="xml", short_empty_elements=True)