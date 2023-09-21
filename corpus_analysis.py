from KorAPClient import KorAPConnection
bunc = KorAPConnection(KorAPUrl = "http://localhost:64543/", verbose=True)
dereko = KorAPConnection(verbose = True)

q = bunc.corpusQuery("[ud/l=голям] [ud/p=NOUN]", metadataOnly=False)
q = q.fetchAll(verbose=True)
print(q)


r = dereko.corpusQuery("[tt/l=groß] [tt/p=NN]", metadataOnly=False)
r = r.fetchNext(verbose=True)
print(r)