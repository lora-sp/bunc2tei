from KorAPClient import KorAPConnection
bunc = KorAPConnection(KorAPUrl = "http://localhost:64543/", verbose=True)
dereko = KorAPConnection(verbose = True)


np_nehmen = dereko.collocationAnalysis("focus([tt/p=NN] {[tt/l=nehmen]})",
                                   leftContextSize = 1,
                                   rightContextSize = 0,
                                   exactFrequencies=False,
                                   searchHitsSampleLimit=1000,
                                   topCollocatesLimit=20)


vzemam_np = bunc.collocationAnalysis("focus({[ud/l=вземам]} [ud/p=NOUN])",
                                   leftContextSize=0,
                                   rightContextSize=1,
                                   exactFrequencies=False,
                                   searchHitsSampleLimit=1000,
                                   topCollocatesLimit=20)


