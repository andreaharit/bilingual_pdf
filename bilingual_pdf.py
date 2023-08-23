import fitz # PyMuPDF 1.22.2, handles reading a pdf
import json
import os # checks if file path is ok
import webbrowser # open pdf in app
import translators as ts # translation tool


def main():
    # initiate variables
    source_processed = {} # dict stores original text {page: [paragraph 1, paragraph 2 etc]}
    translated_processed = {} # dict stores translated text {page: [translated paragraph 1, etc]}

    # gets pdf file path from user and check if it's valid
    valid_file_path = input_file()

    # asks user for translation engine
    user_eng = user_chosen_eng()     

    # if user wants, displays supported languages according to the engine 
    answer = asks_user_supported_lang(user_eng)
    if answer:
        open_supported(user_eng)

    # gets target language from user
    user_lang = user_chosen_lang(user_eng)

    # transforms pdf into 2 dict: one with original text, other with translated    
    try: 
        source_processed, translated_processed = source_builder(valid_file_path, user_lang, user_eng)
    except Exception:
        raise Exception ("Something unexpected happened! File could not be translated\n")             
     
    # TO DO: asks user for path to new pdf and name

    # TO DO: builds a new pdf with the table showing paragraph ID, original text and translated
    print("Preparing Bilingual pdf!\n")

    # TO DO: opens new pdf


    # builds a json file
    # with open('clean_original3.json', 'w', encoding = 'utf-8') as output:
    # json.dump(source, output, ensure_ascii = False, indent=4)

# FUNCTIONS

# ask user for original PDF file path
def input_file():        
    while True:
            try:
                file_path = input("Please insert the PDF file path to be translated: ")
                valid_file_path = get_file(file_path)  # check if file path and PDF is valid        
                return valid_file_path     
            except (ValueError, FileExistsError):
                pass

# tests validy of PDF file provided
def get_file(file_path):  
    file_path.strip()

    if (file_path.endswith('.pdf')):  # is it a .pdf?
        if (os.path.isfile(file_path)):  # is it a valid file path? (maybe redundant?)
            try:
                doc = fitz.open(file_path)  # is it a readable file?
                return file_path
            except:
                raise FileExistsError("Corrupted pdf.\n")
        else:
            raise FileExistsError("File path not valid.\n")
    else:
        raise ValueError("File must be in .pdf format.\n")
    

# gets user choice for search engine
def user_chosen_eng():
    engines = { 
        "google":["g", "google"],
        "deepl":["d","deepl"]
        }
    while True:
        try:
            answer = input("Please choose a search engine Google or Deepl. Type G or D:").lower().strip()            
            for e_key, e_value in engines:
                if answer in e_value:
                    return e_key
                else:
                    raise ValueError   
        except ValueError:
            print ("Answer not recognized.\n")
            pass
    
# Asks user if they want to see supported languages
def asks_user_supported_lang(engine):
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
def open_supported(engine): 
    supported = {"google":"supported_google.pdf",
                 "deepl": "supported_deepl.pdf"}   
    if engine in supported:
        file = supported[engine]
        webbrowser.open(file)
        return True 
    else:
        raise ValueError 
        
# Gets user target language and returns the language code accepted by translators
# Obs: function made this way so I can practice pytest monkeypatch and a new way of looping  
def user_chosen_lang(engine):
    eng_files = {"google":"supported_google.json",
                 "deepl": "supported_deepl.json"}  
 
    # asks user lang choice    
    user_lang = input ("Choose your language: \n") 
    user_lang = user_lang.lower().strip()

    # load supported languages according to chosen engine
    if engine in eng_files:
        f = open (eng_files[engine]) # open a pdf with supported languages in user default app  
        supported =  json.load(f)    
    else:
        raise ValueError

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
    print ("No language found.\n")
    asks_user_supported_lang()
    return user_chosen_lang()   


# Extracts pages and paragraphs from original pdf, transforming in dictionary. TESTED
def source_builder(document, user_lang):  
    # variables initialization
    n_page = 1  # page counter, starts in 1 to be user friendlier
    # dicts to hold original and translated: key is page's number, elements are its paragraphs
    translated = {}
    original = {} 

    # open, read and populate dictionary
    doc = fitz.open(document)   
    for page in doc:
        # provisory list of paragraphs in each page
        provisional_original = [] 
        provisional_translated = [] 

        # reads each "block" in the page, aka list with characteristics and content of a paragraph
        source = page.get_text("blocks")     
        for paragraph in source:
            if (paragraph[6] == 0):  # ignores blocks that are type "image"               
                sentence = p_cleaner(paragraph[4]) # clean paragraph of weird markdown/special char stuff                
                if sentence != "" or sentence != "\n": # ignores blank paragraphs
                    # keeps populating provisory lists in current page
                    provisional_original.append(sentence)                                 
                    provisional_translated.append(translate(sentence, user_lang)) 

        # after provisory list is done:
        # builds dict with that page number as key and its list of paragraphs as values           
        original[n_page] = provisional_original        
        translated[n_page] = provisional_translated
        
        # and let's do the next page then
        n_page = n_page + 1
    return original, translated

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
