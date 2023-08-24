import translators as ts

sentence = "Hi how are you?"
engine = "google"
language = "EN"

translation = ts.translate_text(query_text = sentence, translator = engine, from_language = 'auto', to_language=language)        

print(translation)