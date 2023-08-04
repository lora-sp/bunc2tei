import sys
from turtle import setx
import xml.etree.ElementTree as ET
from tqdm import tqdm


def main():
    corpusRoot = ET.Element("teiCorpus")

    for j in tqdm(range(1, len(sys.argv))):
        try:
            doc_data, genre = extract_data(sys.argv[j])
            doc_tree = create_tree(doc_data, genre, j-1)
            currentRoot = doc_tree.getroot()
            corpusRoot.append(currentRoot)
        except:
            print("Warning: could not parse file: " + sys.argv[j], file=sys.stderr) 
            continue

    corpusTree = ET.ElementTree(corpusRoot)
    ET.indent(corpusTree, "  ")
    corpusTree.write(sys.stdout, encoding='unicode')


def extract_data(file):
    ''' Parses an xml file and saves the metadata and texts into a dictionary that is returned.
    The dictionary is of the following form:
    Online newspaper:
    data = {filenumber: {title}, {url}, {author}, {date}, {time}, {text}}
    Literature: 
    data = {filenumber: {title}, {url}, {author}, {year}, {text}}
    Parliament debate: 
    data = {filenumber: {speaker, {gender}, {date}}}
    '''
    
    
    tree = ET.parse(file)
    root = tree.getroot()
    ET.register_namespace("", "http://www.tei-c.org/ns/1.0")
    

    data = {}
    genre = {}

    
    if root.find("{http://www.tei-c.org/ns/1.0}text").get('source').endswith('.bg') or \
        root.find("{http://www.tei-c.org/ns/1.0}text").get('source') == 'chitanka.info' :
        
        
        for i, text in enumerate(root.iter("{http://www.tei-c.org/ns/1.0}text")):


            if text.get('source').endswith('.bg'):

                genre[i] = "news"
                data[i] = {}
                data[i]['title'] = text.get('title')
                data[i]['url'] = text.get('url')
                data[i]['author'] = text.get('author') 
                data[i]['date'] = text.get('date').split(' ')[0]
                data[i]['time'] = text.get('date').split(' ')[1]

                textelem = text.find(".{http://www.tei-c.org/ns/1.0}body/{http://www.tei-c.org/ns/1.0}div/"\
                                    "{http://www.tei-c.org/ns/1.0}div")
            
                data[i]['text'] = []
                for p in textelem.findall(".{http://www.tei-c.org/ns/1.0}p"):
                    data[i]['text'].append(p)

            elif text.get('source') == 'chitanka.info':

                genre[i] = "lit"
                data[i] = {}
                data[i]['title'] = text.get('title')
                data[i]['url'] = text.get('url')
                data[i]['author'] = text.get('author')
                data[i]['year'] = text.get('date')
                data[i]['genre'] = text.get('category')

                textelem = text.find(".{http://www.tei-c.org/ns/1.0}body/{http://www.tei-c.org/ns/1.0}div/"\
                                    "{http://www.tei-c.org/ns/1.0}div")
                
                data[i]['text'] = []
                for p in textelem.findall(".{http://www.tei-c.org/ns/1.0}p"):
                    data[i]['text'].append(p)

    else:

        for i, u in enumerate(root.iter("{http://www.tei-c.org/ns/1.0}u")):

            genre[i] = "parl"
            data[i] = {}
            data[i]['speaker'] = u.get('who')
            data[i]['sex'] = u.get('sex')
            data[i]['date'] = file

            data[i]['text'] = []
            for seg in u.findall(".{http://www.tei-c.org/ns/1.0}seg"):
                    seg.tag = "p" 
                    data[i]['text'].append(seg)
    
    return data, genre

def extract_name(string):
    ''' Takes strings from ParlaMint corpus that indicate the speaker names and outputs them
    in the format {first name} {last name}.
    '''

    lastname = ""
    firstname = ""

    lastname += string[1]

    for char in string[2:]:

        if not char.isupper() and len(firstname) == 0:
            lastname += char
        
        elif char.isupper():
            firstname += char

        else:
            firstname += char
    
    return firstname + " " + lastname

def create_tree(data, genre, filenumber):
    ''' Receives a dictionary containing the data and returns an xml tree in the 
    desired format, according to each genre. Generates text sigles of the following format: BNC/filenumber.textnumber,
    e.g. BNC/000.00000
    '''
    docRoot = ET.Element("teiDoc")

    for i in range(len(data)):

        if genre[i] == "news":

            tei = ET.SubElement(docRoot, "TEI")
            teiHeader = ET.SubElement(tei, "teiHeader")
            fileDesc = ET.SubElement(teiHeader, "fileDesc")
            titleStmt = ET.SubElement(fileDesc, "titleStmt")
            textSigle = ET.SubElement(titleStmt, "textSigle")
            textSigle.text = "BNC/" + f"{filenumber:03}" + "." + f"{i:05}"
            sourceDesc = ET.SubElement(fileDesc, "sourceDesc")
            analytic = ET.SubElement(sourceDesc, "analytic")
            htitle = ET.SubElement(analytic, "h.title")
            htitle.text = data[i]['title']
            hauthor = ET.SubElement(analytic, "h.author")
            hauthor.text = data[i]['author']
            imprint = ET.SubElement(sourceDesc, "imprint")
            pubDateYear = ET.SubElement(imprint, "pubDate")
            pubDateYear.set("type", "year")
            pubDateYear.text = data[i]['date'][0:4]
            pubDateMonth = ET.SubElement(imprint, "pubDate")
            pubDateMonth.set("type", "month")
            pubDateMonth.text = data[i]['date'][5:7]
            pubDateDay = ET.SubElement(imprint, "pubDate")
            pubDateDay.set("type", "day")
            pubDateDay.text = data[i]['date'][8:10]
            pubDateTime = ET.SubElement(imprint, "pubDate")
            pubDateTime.set("type", "time")
            pubDateTime.text = data[i]['time']
            pubPlace = ET.SubElement(imprint, "pubPlace")
            ref = ET.SubElement(pubPlace, "ref")
            ref.set("type", "page_url")
            ref.set("target", data[i]['url'])
            text = ET.SubElement(tei, "text")
            body = ET.SubElement(text, "body")
            for p in data[i]['text']:
                body.append(p)

        elif genre[i] == "lit":

            tei = ET.SubElement(docRoot, "TEI")
            teiHeader = ET.SubElement(tei, "teiHeader")
            fileDesc = ET.SubElement(teiHeader, "fileDesc")
            cat = ET.SubElement(teiHeader, "category")
            catDesc = ET.SubElement(cat, "catDesc")
            catDesc.text = data[i]['genre'] 
            titleStmt = ET.SubElement(fileDesc, "titleStmt")
            textSigle = ET.SubElement(titleStmt, "textSigle")
            textSigle.text = "BNC/" + f"{filenumber:03}" + "." + f"{i:05}"
            sourceDesc = ET.SubElement(fileDesc, "sourceDesc")
            analytic = ET.SubElement(sourceDesc, "analytic")
            htitle = ET.SubElement(analytic, "h.title")
            htitle.text = data[i]['title']
            hauthor = ET.SubElement(analytic, "h.author")
            hauthor.text = data[i]['author']
            imprint = ET.SubElement(sourceDesc, "imprint")
            pubDateYear = ET.SubElement(imprint, "pubDate")
            pubDateYear.set("type", "year")
            pubDateYear.text = data[i]['year']
            pubPlace = ET.SubElement(imprint, "pubPlace")
            ref = ET.SubElement(pubPlace, "ref")
            ref.set("type", "page_url")
            ref.set("target", data[i]['url'])
            text = ET.SubElement(tei, "text")
            body = ET.SubElement(text, "body")
            for p in data[i]['text']:
                body.append(p)

        else:

            tei = ET.SubElement(docRoot, "TEI")
            teiHeader = ET.SubElement(tei, "teiHeader")
            fileDesc = ET.SubElement(teiHeader, "fileDesc")
            titleStmt = ET.SubElement(fileDesc, "titleStmt")
            textSigle = ET.SubElement(titleStmt, "textSigle")
            textSigle.text = "BNC/" + f"{filenumber:03}" + "." + f"{i:05}"
            sourceDesc = ET.SubElement(fileDesc, "sourceDesc")
            analytic = ET.SubElement(sourceDesc, "analytic")
            speaker = ET.SubElement(analytic, "speaker")
            speaker.text = extract_name(data[i]['speaker'])
            speaker.set('sex', data[i]['sex']) #????????
            imprint = ET.SubElement(sourceDesc, "imprint")
            pubDateYear = ET.SubElement(imprint, "pubDate")
            pubDateYear.set("type", "year")
            pubDateYear.text = data[i]['date'][-14:-10]
            pubDateMonth = ET.SubElement(imprint, "pubDate")
            pubDateMonth.set("type", "month")
            pubDateMonth.text = data[i]['date'][-9:-7]
            pubDateDay = ET.SubElement(imprint, "pubDate")
            pubDateDay.set("type", "day")
            pubDateDay.text = data[i]['date'][-6:-4]
            text = ET.SubElement(tei, "text")
            body = ET.SubElement(text, "body")
            for seg in data[i]['text']:
                body.append(seg)
        

    docTree = ET.ElementTree(docRoot)
    ET.indent(docTree, "  ")

    return docTree


main()