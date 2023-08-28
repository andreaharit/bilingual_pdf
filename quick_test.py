import translators as ts

example ={"1":["oi tudo bem?"], "2":["primeiro teste", "outro teste"]}
lang = "en"
eng = "google"

def translator_builder(original, lang, eng):  
    trans ={}   
    # goes to each key and it's paragraphs and returns a dict with translation
    for page, paragraphs in original.items():
        provisory = []
        for i in paragraphs:
            new_sentence = translate(i, lang, eng)
            provisory.append(new_sentence)
        trans[page] = provisory 

    return trans                          
           

def translate(paragraph, language, engine): 
    # uses google translate            
    try:
        translation = ts.translate_text(query_text = paragraph, translator = engine, from_language = 'auto', to_language=language)        
    except Exception:       
        translation = "ERROR: Could not translate, sorry!\n"
    return translation

final = translator_builder(example, lang, eng)

print (final)