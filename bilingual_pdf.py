import fitz # PyMuPDF 1.22.2, handles reading a pdf
import json
import webbrowser # open pdf in app
import translators as ts # translation tool
import sys


def main():
    # initiate variables
    source_processed = {} # dict stores original text {page: [paragraph 1, paragraph 2 etc]}
    translated_processed = {} # dict stores translated text {page: [translated paragraph 1, etc]}

    # gets pdf file path from user and check if it's valid
    valid_file_path = input_file()

    # asks user for translation engine
    user_eng = user_chosen_eng()     

    # if user wants, displays supported languages according to the engine 
    answer = asks_see_supported(user_eng)
    if answer:
        open_supported_file(user_eng)

    # gets target language from user
    user_lang = user_chosen_lang(user_eng)

    print("Preparing Bilingual pdf! This might take a bit =)\n")


    # transforms pdf into 2 dict: one with original text, other with translated    
    try: 
        source_processed, translated_processed, paragraphs = source_builder(valid_file_path, user_lang, user_eng)
    except Exception:
        raise Exception ("Something unexpected happened! File could not be translated")             
     
    # TO DO: asks user for path to new pdf and name

    # TO DO: builds a new pdf with the table showing paragraph ID, original text and translated

    # TO DO: opens new pdf


    # builds a json file for testing
    with open('original.json', 'w', encoding = 'utf-8') as one:
        json.dump(source_processed, one, ensure_ascii = False, indent=4)
    with open('translated.json', 'w', encoding = 'utf-8') as two:
        json.dump(translated_processed, two, ensure_ascii = False, indent=4)
    print (paragraphs)

# FUNCTIONS

# ask user for original PDF file path TESTED
def input_file():        
    while True:
            try:
                file_path = input("Please insert the PDF file path to be translated: ")
                valid_file_path = check_file(file_path)  # check if file path and PDF is valid        
                return valid_file_path     
            except FileExistsError:
                print("Error loading the file, please check the file path and if the file is a PDF.\n")
                pass

# tests validy of PDF file provided TESTED
def check_file(file_path):  
    file_path.strip()
    try: 
        doc = fitz.open(file_path)  # is it a readable file?
        return file_path
    except Exception:
        raise FileExistsError   

# gets user choice for search engine TESTED
def user_chosen_eng():
    engines = {
        "g":"google",
        "d":"deepl"
        }   
    while True:
        try:            
            answer = input("Please choose a search engine Google or Deepl. Type G or D:").lower().strip()            
            if answer in engines.keys():
                return engines[answer] 
            elif answer in engines.values():
                return answer
            else:                 
                raise ValueError
        except ValueError:
            print ("Answer not recognized.\n")
            pass
    
# Asks user if they want to see supported languages TESTED
def asks_see_supported(engine="google"):
    # supported answers 
    yes = ["y", "yes"]
    no = ["n", "no"] 

    while True:
        try:
            answer = input("Would you like to know the possible languages? Please type Y or N: ").lower().strip()
            if answer in yes:
                return True
            elif answer in no:
                return False
            else: 
                raise ValueError               
        except ValueError:
            print ("Please type Y or N.\n")
            pass

# Opens PDF with supported languages according to chosen engine
def open_supported_file(engine): 
    supported = {"google":"supported_google.pdf",
                 "deepl": "supported_deepl.pdf"}   
    if engine in supported:
        file = supported[engine]
        webbrowser.open(file)
        return True 
    else:
        raise ValueError 

# Ask user to input target language for translation

def user_chosen_lang(engine):
    while True:
        try:
            user_lang = input ("Please type the languague you want to translate to: ").lower().strip() 
            lang_code = validadate_lang(user_lang, engine)
            return lang_code
        except ValueError:
            print ("No language found. Let's try again!\n")
            asks_see_supported()
            pass
        except ImportError:
            print ("Fatal Error loading language file.\n")
            sys.exit()
            
        
# Validate user typed language, and returns the language code accepted by translators
# Obs: function made this way so I can practice pytest monkeypatch and a new way of looping  
def validadate_lang(user_lang, engine):
    eng_files = {"google":"supported_google.json",
                 "deepl": "supported_deepl.json"}   
    
    # load supported languages according to chosen engine
    try:        
        f = open (eng_files[engine]) # open the json with supported languages for given engine  
        supported =  json.load(f)    
    except Exception:        
        raise ImportError

    # sees if user input is recognized inside that json
  
    if user_lang in supported.keys(): # user typed alredy the language code? ex "en" 
        chosen_language = user_lang         
        f.close()
        return chosen_language           
    else: # user typed the long version? ex "English"
        user_lang = user_lang.title() # formating to match the json style
        for code, names in supported.items():                
            if type(names) != list: # if there is just one way of naming the lang (some langs have many)
                names = [names] # tuns into list, so folloring line can check for langs with one or multiple names                     
            if user_lang in names:  # then checks names in lists for match with user input, returning the code
                chosen_language = code               
                f.close()
                return chosen_language
    raise ValueError

# Extracts pages and paragraphs from original pdf, transforming in dictionary. TESTED

def source_builder(document, lang, eng):  
    # variables initialization
    n_page = 1  # page counter, starts in 1 to be user friendlier
    p = [] # stores number of paragraphs per page

    # dicts to hold original and translated: key is page's number, elements are its paragraphs
    translated = {}
    original = {} 

    # open, read and populate dictionary
    doc = fitz.open(document)   
    for page in doc:
        # provisory list of paragraphs in each page
        provisional_original = [] 
        provisional_translated = [] 
        par = 0 # provisional paragraph counter per page

        # reads each "block" in the page, aka list with characteristics and content of a paragraph
        source = page.get_text("blocks")     
        for paragraph in source:
            if (paragraph[6] == 0):  # ignores blocks that are type "image"               
                sentence = p_cleaner(paragraph[4]) # clean paragraph of weird markdown/special char stuff                
                if sentence != "" or sentence != "\n": # ignores blank paragraphs
                    # keeps populating provisory lists in current page
                    provisional_original.append(sentence)                                 
                    provisional_translated.append(translate(sentence, lang, eng)) 
                    par = par + 1
        # after provisory list is done:
        # update list of number of paragraphs in each page
        p.append(par) 
        # builds dict with that page number as key and its list of paragraphs as values        
        original[n_page] = provisional_original        
        translated[n_page] = provisional_translated
        n_page = n_page + 1
    return original, translated, p

# TO DO: there are other leftover characters not cleaned yet 
# to think: should I ignore paragraphs that are just websites, dates, numbers?
def p_cleaner(paragraph):  # Clean paragraphs texts of weird leftover characters
    new = paragraph.rstrip("\n").replace("\n", " ").replace("  ", " ").strip().replace('\"',"'")    
    return new

def hf_cleaner(): # TO DO clean dictionary with original from possible repetitive footers and headers
    print("something")

# Translate each paragraph, TESTED    
def translate(paragraph, language, engine): 
    # uses google translate            
    try:
        translation = ts.translate_text(query_text = paragraph, translator = engine, from_language = 'auto', to_language=language)        
    except Exception:       
        translation = "ERROR: Could not translate, sorry!\n"
    return translation


# TO DO Build new pdf using table to shape content
# (column 1 is page.paragraph number, 2 is original, 3 is translated)

# to make it fancy: 
# GUI interface? Choice of translator? Option to print separate original page and translated?

if __name__ == "__main__":
    main()
