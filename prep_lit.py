import sys, os
import xml.etree.ElementTree as ET
from lingua import Language, LanguageDetectorBuilder
from tqdm import tqdm

for i in tqdm(range(1, len(sys.argv))):

	# Parse file and extract root
	filetext = ""
	tree = ET.parse(sys.argv[i])
	ET.register_namespace("", "http://www.tei-c.org/ns/1.0")
	root = tree.getroot()

	# Delete file if <p>-elements are empty
	if all(False for elem in root.iter("{http://www.tei-c.org/ns/1.0}p")):
		print("Warning: file contains only metadata. Deleted " + sys.argv[i], file=sys.stderr) 
		os.remove(sys.argv[i])
		continue
		
	# Append text to one continuous string
	while filetext == "":
		for elem in root.iter("{http://www.tei-c.org/ns/1.0}p"):
		    filetext += elem.text

	# Detect most prominent language in the text
	languages = [Language.BULGARIAN, Language.ENGLISH]
	detector = LanguageDetectorBuilder.from_languages(*languages).build()
	lang = detector.detect_language_of(filetext)

	# Delete file if most prominent language is not Bulgarian
	if lang != Language.BULGARIAN:
		print("Warning: file not Bulgarian. Deleted " + sys.argv[i], file=sys.stderr) 
		os.remove(sys.argv[i])

