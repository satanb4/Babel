import apertium

def translate():
    # data = data.split()
    translator = apertium.Translator('en','spa')
    translated = translator.translate('cat')
    return translated
