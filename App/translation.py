import apertium

def tranSetup(lang1,lang2):
    tranLanguages = {('eng','spa'),('bel','rus'),('br','fr'),('cym','eng'),
    ('eng','cat'),('dan','nor'),('eng','kaz'),('en','gl'),('es','pt'),('fr','es'),('kaz','rus'),
    ('spa','ita'),('swe','dan'),('urd','hin')}
    
    for langPair in tranLanguages:
        if (lang1 and lang2) in langPair:
            return langPair[0],langPair[1] 

def translate(data):
    translator = apertium.Translator('eng','spa')
    translated = translator.translate(data)
    return translated
