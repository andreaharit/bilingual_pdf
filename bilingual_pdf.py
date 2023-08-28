import fitz # PyMuPDF handles parsing the pdf
import webbrowser # Ppen pdf for user
import translators as ts # Translation library
import re
import json


# TO DO: there are a lot of characters remaining to be clean, source builder is appending empty stuff
# make the final pdf


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
    user_lang, lang_name = user_chosen_lang(user_eng)

    # sums up to user all the info
    print("Great, we are translating now " + valid_file_path + " to " + lang_name + ".\n")
    print("Preparing Bilingual pdf! This might take a bit =)\n")


    # transforms pdf into 2 dict: original text, translated and count paragraphs per page    
    try: 
        source_processed, paragraphs = source_builder(valid_file_path)
        translated_processed = translator_builder (source_processed, user_lang, user_eng)
    except Exception:
        raise Exception ("Something unexpected happened! File could not be translated.")            
     

    # TO DO: builds a new pdf with the table showing paragraph ID, original text and translated

    # TO DO: opens new pdf to user


    # builds a json file for testing
    with open('original.json', 'w', encoding = 'utf-8') as one:
        json.dump(source_processed, one, ensure_ascii = False, indent=4)
    with open('translated.json', 'w', encoding = 'utf-8') as two:
        json.dump(translated_processed, two, ensure_ascii = False, indent=4)
    print (paragraphs)
    print ("It worked! Go check =) \n")


# FUNCTIONS

# Asks user for PDF file path TESTED
def input_file():        
    while True:
            try:
                file_path = input("Please insert the PDF file path to be translated: ")
                valid_file_path = check_file(file_path)  # check if file path and if is a valid PDF       
                return valid_file_path     
            except FileExistsError:
                print("Error loading the file, please check the file path or if file is a PDF.\n")
                pass


# Tests validy of PDF file/filepath TESTED
def check_file(file_path):  
    file_path.strip()
    try: 
        doc = fitz.open(file_path)  # is it a readable file?
        return file_path
    except Exception:
        raise FileExistsError   


# Asks user for search engine TESTED
# PS: translator library is having issues with deepl, so this option is commented until this is solved
def user_chosen_eng():
    engines = {
        "g":"google",
        "b":"bing"
        # "d":"deepl"
        }   
    while True:
        try:            
            answer = input("Please choose a search engine: Google or Bing.\nType it's first letter G or B:").lower().strip()            
            if answer in engines.keys():
                return engines[answer] 
            elif answer in engines.values():
                return answer
            else:                 
                raise ValueError
        except ValueError:
            print ("Answer not recognized.\n")
            pass


# Asks user if they want to see supported languages for chosen engine TESTED
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


# Opens PDF with supported languages according to chosen engine TESTED
def open_supported_file(engine = "google"): 
    supported = {"google":"supported_google.pdf",
                 "bing":"supported_bing.pdf"                 
                 #"deepl": "supported_deepl.pdf"
                 }   
    if engine in supported:
        file = supported[engine]
        webbrowser.open(file)
        return True 
    else:
        raise ValueError 


# Asks user to input target language for translation TESTED
def user_chosen_lang(engine):
    while True:
        try:
            user_lang = input ("Please type the languague you want to translate to: ").strip().lower()            
            lang_code, languague = validadate_lang(user_lang, engine)
            return lang_code, languague
        except ValueError:
            print ("No language found.\nLet's try again!\n")
            asks_see_supported()
            pass

            
        
# Validate user lang input, and returns the language code accepted by translators TESTED
def validadate_lang(user_lang, engine = "google"):
    eng_files = {"google":"supported_google.json",
                 "bing":"supported_bing.json"
                 #"deepl": "supported_deepl.json"
                 }   
    
    # load supported languages according to chosen engine
    try:        
        f = open (eng_files[engine]) # open the json with supported languages for given engine  
        supported =  json.load(f)    
    except Exception:        
        raise ImportError

    # sees if user input is supported by the engine
    try:
        if user_lang in supported.keys(): # user typed alredy the language code? ex "en" 
            lang_code = user_lang       
        else: # user typed the long version? ex "English"
            for code, names in supported.items():                
                if type(names) != list: # if there is just one name for the lang (some langs have many)
                    names = [names] # tuns into list, so folloring line can check for langs with one or multiple names                     
                if user_lang in names:  # then checks names in lists for match with user input
                    lang_code = code      
            
        # getting language in full name to print to user    
        if type(supported[lang_code]) is not list:        
            language = supported[lang_code] # user typed code, language has only one way of naming
        else:
            language = supported[lang_code][0] # user typed code, language has many names
        
        f.close()         
        # returns the code for the transaltion engine, and a lang name     
        return lang_code, language
    except Exception:
        raise ValueError
    
# Extracts pages and paragraphs from original pdf, transforming in dictionary
def source_builder(document):  
    # variables initialization
    n_page = 1  # page counter, starts in 1 to be user friendlier
    p = [] # stores number of paragraphs per page


    # dicts to hold original: key is page's number, elements are its paragraphs
    original = {} 

    # open, read and populate dictionary
    doc = fitz.open(document) 

    for page in doc:
        provisional_original = [] # provisory list of paragraphs for each page
        n_par = 0 # provisional counter of number of paragraph for each page

        # reads each "block" in the page, see PyMuPDF documentation
        source = page.get_text("blocks")     
        for paragraph in source:
            if (paragraph[6] == 0):  # ignores blocks that are type "image"               
                sentence = p_cleaner(paragraph[4]) # clean weird chars or paragraphs that don't have real text               
                if sentence != "" or sentence != "\n": # ignores blank paragraphs
                    # populating provisory lists in current page
                    provisional_original.append(sentence)                                 
                    n_par = n_par + 1
        
        # update list of number of paragraphs in each page
        p.append(n_par) 
        # builds dict with that page number as key and its list of paragraphs as values        
        original[n_page] = provisional_original        
        n_page = n_page + 1
    return original, p

# Translates the dictionary with original text
def translator_builder(original, lang, eng): 
    source = original 
    trans ={}   
    # goes to each key and it's paragraphs and returns a dict with translation
    for page, paragraphs in source.items():
        provisory = []
        for i in paragraphs:
            new_sentence = translate(i, lang, eng)
            provisory.append(new_sentence)
        trans[page] = provisory 
    return trans  



# Cleans parser's special char, websites and string that contain no real text 
def p_cleaner(paragraph):  # Clean paragraphs texts of weird leftover characters
    new = paragraph.rstrip("\n").replace("\n", " ").replace("  ", " ").strip().replace('\"',"'") 

    if re.search(r"http|www", paragraph): # check if there is url and substitute for shorter "URL"
        s = re.sub("http\S+","URL", paragraph)
        s = re.sub("www\S+","URL", s)
        mod_sentence = s.replace("URL", "1").strip() # gimmick to see if sentence will be just url + garbage
    else:
        mod_sentence = paragraph

    for c in mod_sentence: #checking if the sentence has just numbers, special char, url 
        if c.isalpha():
            check = True
            break
        else:
            check = False
    if check: # sentence has real words
        new = mod_sentence
    else: # if it's a garbage sentence returns empty string
            new=""
    
    return new

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
