import apertium

def tranSetup():
    pass

def translate(data):
    analyzer = apertium.Analyzer('en')
    analyzed = analyzer.analyze(data)
    # translator = apertium.Translator('en','spa')
    # translated = translator.translate('cat')
    return analyzed
