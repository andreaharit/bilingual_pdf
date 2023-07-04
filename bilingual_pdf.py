import fitz # PyMuPDF 1.22.2, handles reading a pdf
import json
import os # checks if file path is ok
import webbrowser # open pdf in app
import translators as ts # translation tool


def main():
    # initiale variables
    source_processed = {} # dict stores original text {page: [paragraph 1, paragraph 2 etc]}
    translated_processed = {} # dict stores translated text {page: [translated paragraph 1, etc]}
    

    # gets pdf document from user 
    while True:
        try:
            file_path = input("Please insert the PDF file path to be translated: \n")
            valid_file_path = get_file(file_path)        
            break    
        except (ValueError, FileExistsError):
            pass

    print("We will now select the target language for translation.\n")

    # displays, if user chooses, supported languages
    while True:
        try:
            info = input("First, would you like to know the possible languages? Please type Y or N.\n")
            user_possible_lang(info) 
            break           
        except (ValueError):
            pass

    # gets target language from user
    # obs: this was done without the "while true try" so I can practice something new
    user_lang = user_chosen_lang()     

             
    # transforms pdf into 2 dict: one with original text, other with translated    
    try: 
        source_processed, translated_processed = source_builder(valid_file_path, user_lang)
    except Exception:
        raise Exception ("Something unexpected happened! File could not be translated\n")             
     

    # building new pdf
    print("Preparing Bilingual pdf!\n")

    # outputting new pdf

    # builds a json file
    # with open('clean_original3.json', 'w', encoding = 'utf-8') as output:
    # json.dump(source, output, ensure_ascii = False, indent=4)

# FUNCTIONS

# tests validy of pdf file from user, TESTED
def get_file(file_path):  
    file_path.lower().strip()
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

# Asks user if they want to see the supported languages, TESTED
def user_possible_lang(info): 
    # supported answers 
    yes = ["y", "yes"]
    no = ["n", "no"]  
    info = info.lower().strip()  

    if info in yes:
        webbrowser.open(r'languages_info.pdf') # open a pdf with supported languages in default user app  
        return True              
    elif info in no:
        return True              
    else: # if user types wrong stuff
        print ("Please type Y or N.\n")
        raise ValueError
        
# Gets user input of target language
# Obs: it has input inside so I can practice pytest monkeypatch and a new way of looping  
def user_chosen_lang(user_lang): 
    # asks user lang choice
    lang = input ("Choose your language: \n") 
    lang = lang.lower().strip()

    # load supported languages
    f = open('supported_languages.json')
    lang_file =  json.load(f)

    # sees if user input is recognized in the supported languages
    if lang in lang_file.keys(): # if it's the short version of the language ex "en" 
        chosen_language = lang         
        f.close()
        return chosen_language           
    else: # if user typed the long version of the language's name ex "English"
        lang = lang.title() # formating to match the json with supported languages
        for lang_key, item in lang_file.items():
            if type(item) != list: # if there is just one supported way of naming it
                item = [item] # tuns into list fro checking, some langs have more names                       
            if lang in item:  # checks list of lang names to see if matches the supported ones
                chosen_language = lang_key               
                f.close()
                return chosen_language             
    print ("No language found.\n")
    info = input("Would you like to know the possible languages? Please type Y or N.\n")
    user_possible_lang(info) 
    user_lang()    
         

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
        p_list_original = [] 
        p_list_translated = [] 

        # reads each "block" in the page, aka list with characteristics and content of a paragraph
        source = page.get_text("blocks")     
        for paragraph in source:
            if (paragraph[6] == 0):  # ignores blocks that are type "image"               
                sentence = p_cleaner(paragraph[4]) # clean paragraph of weird markdown/special char stuff                
                if sentence != "" or sentence != "\n": # ignores blank paragraphs
                    # keeps populating provisory lists in current page
                    p_list_original.append(sentence)                                 
                    p_list_translated.append(translate(sentence, user_lang)) 

        # after provisory list is done:
        # builds dict with that page number as key and its list of paragraphs as values           
        original[n_page] = p_list_original        
        translated[n_page] = p_list_translated
        
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

# Functional but TO TEST: translate each paragraph of a dic and build a new one    
def translate(paragraph, language): 
    # uses google translate            
    try:
        translation = ts.translate_text(query_text = paragraph, translator = 'google', from_language = 'auto', to_language=language)        
    except Exception:       
        translation = "ERROR: Could not translate, sorry!\n"
    return translation


# TO DO Build new pdf using table to shape content
# (column 1 is page.paragraph number, 2 is original, 3 is translated)

# to make it fancy: 
# GUI interface? Choice of translator? Option to print separate original page and translated?

if __name__ == "__main__":
    main()
