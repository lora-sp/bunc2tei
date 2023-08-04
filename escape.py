import re
import sys
import xml.etree.ElementTree as ET
from tqdm import tqdm


def escape(file):        
	with open(sys.argv[i], "r+") as f:
		file = f.read()
		replace_symbols = r'&(?!gt;|apos;|quot;|lt;|amp;)|<(?!\/|p>|text|body|div|TEI|\?xml)'

		
		def replace(match):
    			return "&amp;" if match.group().startswith('&') else "&lt;"
		
		file = re.sub(replace_symbols, replace, file)


		f.seek(0)
		f.write(file)
		f.truncate()
	

for i in tqdm(range(1, len(sys.argv))):

	try:
		ET.parse(sys.argv[i])
	except:
		print("Escaped file " + sys.argv[i])
		escape(sys.argv[i])
		try: 
			ET.parse(sys.argv[i])
		except: 
			print("Something else is wrong: " + sys.argv[i])
