import sys, os
import xml.etree.ElementTree as ET
from tqdm import tqdm

persons_tree = ET.parse(sys.argv[1] + "/persons/ParlaMint-BG-listPerson.xml")
persons_root = persons_tree.getroot()
ET.register_namespace("", "http://www.tei-c.org/ns/1.0")

persons = {}

for person in persons_root.iter("{http://www.tei-c.org/ns/1.0}person"):
    name = ""
    for attr, value in person.attrib.items():
        if attr.endswith("id"):
            name = value
            break
    sex = person.find("{http://www.tei-c.org/ns/1.0}sex")
    if sex is None:
        persons[name] = ""
    else:
        persons[name] = sex.get('value')


for filename in tqdm(os.listdir(sys.argv[1])):

    f = os.path.join(sys.argv[1], filename)
    if os.path.isdir(f):
        continue

    tree = ET.parse(f)
    root = tree.getroot()

    for text in root.iter("{http://www.tei-c.org/ns/1.0}text"):
        text.set('source', 'ParlaMint')
    
    for u in root.iter("{http://www.tei-c.org/ns/1.0}u"):
        current_person = u.get('who')[1:]
        u.set('sex', persons[current_person])

    tree.write(f, encoding='unicode')