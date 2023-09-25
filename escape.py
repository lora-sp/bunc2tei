import re
import sys
import xml.etree.ElementTree as ET
from tqdm import tqdm


def escape(file):        
	''' Reads every file from the standard input and looks for unescaped ampersand ('&') and less-than ('<') symbols 
 	wit the help of a regular expression and replaces them with '&amp;' and '&lt;', respectively '''
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
	''' Prints names of the files handled by the escape function. Print message if parsing still fails after escaping. '''
	try:
		ET.parse(sys.argv[i])
	except:
		print("Escaped file " + sys.argv[i])
		escape(sys.argv[i])
		try: 
			ET.parse(sys.argv[i])
		except: 
			print("Something else is wrong: " + sys.argv[i])
