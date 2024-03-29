import sys
import xml.etree.ElementTree as ET
from tqdm import tqdm

genres = []

# Parse each file
for i in tqdm(range(1, len(sys.argv))):
    tree = ET.parse(sys.argv[i])
    root = tree.getroot()
    ET.register_namespace("", "http://www.tei-c.org/ns/1.0")

    # Extract text category by the <category>-element
    for text in root.iter("{http://www.tei-c.org/ns/1.0}text"): 
        genre = text.get('category')
        genre = genre.split('/')

        # Append new genres to list of genres
        if genre[0] not in genres:
            genres.append(genre[0])

print(genres) 
