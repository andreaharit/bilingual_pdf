import json

def user_chosen_lang(engine):
    while True:
        try:
            user_lang = input ("Choose your language: \n").lower().strip() 
            lang_code = validadate_user_lang (user_lang, engine)
            return lang_code
        except ValueError:
            print ("No language found. Let's try again!\n")
            pass
        except ImportError:
            print ("Fatal Error loading language file.\n")
            




def validadate_user_lang(user_lang, engine):
    eng_files = {"google":"supported_google.json",
                 "deepl": "supported_deepl.json"}   
    
    user_lang = user_lang.lower().strip()

    # load supported languages according to chosen engine
    try:        
        f = open (eng_files[engine]) # open a pdf with supported languages in user default app  
        supported =  json.load(f)    
    except Exception:        
        raise ImportError

    # sees if user input is recognized in the supported languages
  
    if user_lang in supported.keys(): # is it already the language code? ex "en" 
        chosen_language = user_lang         
        f.close()
        return chosen_language           
    else: # if user typed the long version, aka names, ex "English"
        user_lang = user_lang.title() # formating to match the json 
        for code, names in supported.items():                
            if type(names) != list: # if there is just one way of naming the lang (some is more)
                names = [names] # tuns into list, so if can be checked in the following line                       
            if user_lang in names:  # then checks names in lists for match
                chosen_language = code               
                f.close()
                return chosen_language
       
    raise ValueError("Language not supported.\n")
            
code = user_chosen_lang("google")
print (code)