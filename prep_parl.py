import sys, os
import xml.etree.ElementTree as ET
from tqdm import tqdm

# Parse file that contains information about the members of the parliament, in this case for extracting their sex
persons_tree = ET.parse(sys.argv[1] + "/persons/ParlaMint-BG-listPerson.xml")
persons_root = persons_tree.getroot()
ET.register_namespace("", "http://www.tei-c.org/ns/1.0")

persons = {}

# Store each person's name as a key and their sex as the corresponding value in a dictionary
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

# 
for filename in tqdm(os.listdir(sys.argv[1])):

    # Skip directories
    f = os.path.join(sys.argv[1], filename)
    if os.path.isdir(f):
        continue

    # Parse file and get root
    tree = ET.parse(f)
    root = tree.getroot()

    # Set new <source>-element to 'ParlaMint' in order to distinguish the genres
    for text in root.iter("{http://www.tei-c.org/ns/1.0}text"):
        text.set('source', 'ParlaMint')

    # Get each speaker per utterance and add their sex as a new attribute, according to the dictionary created above
    for u in root.iter("{http://www.tei-c.org/ns/1.0}u"):
        current_person = u.get('who')[1:]
        u.set('sex', persons[current_person])

    tree.write(f, encoding='unicode')
