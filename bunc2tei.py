import os, sys
import xml.etree.ElementTree as ET
from xml.dom import minidom
from lxml import etree
from io import StringIO


def main():
    # Create corpus structure from string and save into file 
    corpus = "<teiCorpus>\n</teiCorpus>"
    origRoot = ET.fromstring(corpus)
    corpusStr = minidom.parseString(ET.tostring(origRoot)).toprettyxml(indent="  ")
    if not os.path.exists('input'):
        os.makedirs("input")
    if not os.path.exists('output'):
        os.makedirs("output")
    with open("input/tree_structure.xml", "w") as f:
        f.write(corpusStr)

    # Parse corpus tree
    corpusTree = ET.parse("input/tree_structure.xml")
    corpusRoot = corpusTree.getroot()

    # Process documents and append to corpus tree
    for j in range(1, len(sys.argv)):
        try:
            currentTree = convert(j-1, sys.argv[j])
            currentRoot = currentTree.getroot()
            #print(currentRoot.tag)
            corpusRoot.append(currentRoot)
        except:
            print("sorry")
            continue

    # Indent and save tree
    ET.indent(corpusTree, "  ")
    corpusTree.write("output/corpus.p5.xml", encoding='utf-8', xml_declaration=True, method='xml', short_empty_elements=True)


def convert(j, file):
    # Parse document tree and get root
    tree = ET.parse(file)
    root = tree.getroot()
    ET.register_namespace("", "http://www.tei-c.org/ns/1.0")
 
    # Store metadata and texts in lists
    titles = root.findall(".//*[@type='title']")
    #domains = root.findall(".//*[@type='domain']")
    pageURLs = root.findall(".//*[@type='pageURL']")
    #ids = root.findall(".//*[@type='id']")
    #mainImageURLs = root.findall(".//*[@type='mainImageURL']")
    #mainImageTexts = root.findall(".//*[@type='mainImageTexts']")
    #mainImageSources = root.findall(".//*[@type='mainImageSources']")
    authors = root.findall(".//*[@type='authors']")
    #authorURLs = root.findall(".//*[@type='authorURLs']")
    #categories = root.findall(".//*[@type='category']")
    #subCategories = root.findall(".//*[@type='subCategory']")
    #tags = root.findall(".//*[@type='tags']")
    datesPublished = root.findall(".//*[@type='datePublished']")
    timesPublished = root.findall(".//*[@type='timePublished']")
    #datesModified = root.findall(".//*[@type='dateModified']")
    #timesModified = root.findall(".//*[@type='timeModified']")
    #mainImageWidths = root.findall(".//*[@type='mainImageWidth']")
    #mainImageHeights = root.findall(".//*[@type='mainImageHeight']")
    #mainImageThumbnailURLs = root.findall(".//*[@type='mainImageThumbnailURL']")
    texts = []

    # Count text elements and remove metadata
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

    # Remove all elements from root
    for elem in root.findall("*"):
        root.remove(elem)

    # Rename root
    root.tag = "teiDoc"

    # Create target structure
    for i in range(number_of_texts):
        tei = ET.SubElement(root, "TEI")
        teiHeader = ET.SubElement(tei, "teiHeader")
        fileDesc = ET.SubElement(teiHeader, "fileDesc")
        titleStmt = ET.SubElement(fileDesc, "titleStmt")
        textSigle = ET.SubElement(titleStmt, "textSigle")
        textSigle.text = "BNC/" + f"{j:03}" + "." + f"{i:05}"
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
        text = ET.SubElement(tei, "text")
        body = ET.SubElement(text, "body")
        for p in texts[i]:
            body.append(p)

    return tree


main()
