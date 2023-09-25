## Converting various Bulgarian XML-TEI documents into an I5 corpus file

This tool contains various python scripts. The scripts `escape.py`, `prep_lit.py` and `prep_parl.py` are used for preprocessing. The script `explore_lit.py` is used for exploring the literature data set. The script `bunc2tei.py` is used for converting the corpus data into the I5 schema, and the script `test_bunc2tei.py` is a PyTest file to test the conversion script. Finally, the script `corpus_analysis.py` is used for performing a corpus analysis.

### Data

There are three datasets which are handled in this repository. The first consists of online artiles from various Bulgarian newspapers. The second dataset, the so-called Chitanka corpus (`chitanka_esc_prep`), contains literature data from various Bulgarian authors, but also translated pieces, that all belong to different literary text types. The third corpus is the ParlaMint corpus (`parlamint_esc_prep`). It contains parliament debates held in the Bulgarian parliament from 2014 up until 2022. 

### Usage

#### Preprocessing for unescaped symbols: `escape.py`
The script `escape.py` aims at fixing xml files that cannot be processed due to unescaped symbols. This can, for example, be the case for ampersand or "less-than" symbols inside text elements. The script can be executed using `escape.py *.xml`.
1. The script tries to parse the xml files. If the parsing fails, the file is passed to the function `escape`. 
2. `Escape` looks for all `&`-symbols that are not yet escaped and that are not themselves used to escape another symbol using a regular expression (with a negative lookahead) and replaces them with `&amp`.
3. Additionally, the function looks for unescaped `<`-symbols and replaces them with `&lt;`.
4. After replacing, the script tries to parse the files, again. If the parse fails again, it prints "Something else is wrong" including the filename. This indicates that there may be another type of unescaped symbol or another issue that prevents the file from being parsed. 

#### Preprocessing for literature data: `prep_lit.py`
In the Chitanka corpus, several files are either not written in Bulgarian or empty due to copyright complaints. The script `prep_lit.py` tries to detect those files and to remove them from the directory. It is important, however, to first use the preprocessing script `escape.py` before this one, as this sciprt relies on xml parsing being possible. The script can be executed with the command `prep_lit.py *.xml`.
1. An empty string named `filetext` is created. 
2. The file is parsed as an xml file. 
3. If there are no `<p>`-elements in this file, this means that the file consists of metadata, only, and cannot be used for creating the corpus. Therefore, if the condition holds, the files are removed from the directory. 
4. As soon as `filetext` is filled with text, the script tries to detect the main language used in it using the LanguageDetector from the lingua library. If the detected language is not Bulgarian, the file is removed. 

#### Exploring literature data: `explore_lit.py`
The script `explore_lit.py` can be executed with the command `explore_lit.py *.xml`. 
1. It parses each xml file. 
2. It looks for each `category` element, which is used to indicate the type of literature (the genre). 
3. It splits the category at the `/` in order to only consider the first part of the string and to exclude the subategory, and prints a list of the categories. 

#### Preprocessing for ParlaMint data: `prep_parl.py`
The ParlaMint dataset lacks a `source` element indicating the type of document, as opposed to the other two datasets. Therefore, for distinction purposes, it needs to be added. Additionally, the speakers' sex is not encoded in the regular files, but only in the file `ParlaMint-BG-listPerson.xml`. This script takes care of both issues. The script can be executed with the command `prep_parl.py {directory}`, where the directory contains the path to the dataset. 
1. The file `ParlaMint-BG-listPerson.xml` is parsed and a dictionary is created, where each person's name is the key and their sex is the corresponding value. 
2. The script iterates over every file in the directory (that is not a directory itself) and parses the xml documents. Per file, it iterates over each `u` (utterance) element and extracts the speaker.
3. The speaker of each utterance is looked for in the created dictionary, and the corresponding sex is set as an attribute inside each `u` element. 
4. Additionally, the `source` attribute is set to the value `ParlaMint` in order to distinguish each dataset. 

#### Converting the xml files and storing them into one corpus file: `bunc2tei.py`
The script `bunc2tei.py` can be executed with the command `bunc2tei.py *.xml > corpus.p5.xml`. 
1. A new xml tree is created in the main function, with the element `teiCorpus` as its root. The corpus file will be built from it.
2. To build the corpus, each xml file is first passed to the function `extract_data`. `Extract_data` tries to parse the xml file. If the parsing fails, it means the xml file is faulty and needs to be repaired first. This is done by the script `escape.py` and will be explained in the next section. If the parsing succeeds, the relevant data is then extracted by saving the metadata and text elements in a dictionary. The dictionary is then passed to the function `create_tree`. 
3. `Create_tree` creates a new xml tree with the element `teiDoc` as its root. All relevant elements are then inserted at the desired position in the xml tree and filled with the data from the dictionary. 
4. The resulting trees are appended to the corpus tree.
 
#### Testing the conversion tool: `test_bunc2tei.py`
This is a PyTest file. It can be executed by the command `pytest`. This command automatically executes all files that are of the form `test_*.py` or `*_test.py`. The tests are performed on the sample corpus. The script checks whether a set of assumptions are true or false for the output of the script `bunc2tei.py`.

#### Performing a corpus analysis: `corpus_analysis.py`
The script can be executed with the commmand `corpus_analysis.py`. However, in order for it to be executed correctly, the Krill files and the corresponding index are both needed (I can provide these files in case of interest). To initialize KorAP locally, see https://github.com/KorAP/KorAP-Docker. The script uses a localhost address to create an instance of a KorAP-Connection for the Bulgarian corpus and then analyzes it with respect to the given queries. 
