from KorAPClient import KorAPConnection
bunc = KorAPConnection(KorAPUrl = "http://localhost:64543/", verbose=True)
dereko = KorAPConnection(verbose = True)


### 1.: comparing the word много in its noun and adjective modifying functions in Bulgarian

q = bunc.corpusQuery("много [ud/p=NOUN]", metadataOnly=False)
q = q.fetchAll(verbose=True)
print(q)

r = bunc.corpusQuery("много [ud/p=ADJ]", metadataOnly=False)
r = r.fetchAll(verbose=True)
print(r)

### 2.: searching for LVCs in both languages in a collocational analysis

vlizam = bunc.collocationAnalysis("focus({[ud/l=влизам] в} [ud/p=NOUN])",
					leftContextSize = 0,
					rightContextSize = 1, 
					exactFrequencies = False,
					searchHitsSampleLimit=1000,
					topCollocatesLimit = 20)

treten = dereko.collocationAnalysis("focus(in [tt/p=NN] {[tt/l=treten]})",
					leftContextSize = 1,
					rightContextSize = 0, 
					exactFrequencies = False,
					searchHitsSampleLimit=1000,
					topCollocatesLimit = 20)






