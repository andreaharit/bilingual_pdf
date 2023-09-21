import fitz # PyMuPDF handles parsing the pdf
import webbrowser # Ppen pdf for user
import translators as ts # Translation library
import re
import json
from _decimal import Decimal
from borb.pdf import PDF, Document, Page, FlexibleColumnWidthTable, Table, Paragraph, \
     PageLayout, SingleColumnLayout


def main():

    # initiate variables
    source_processed = {} # store original text {page: [paragraph 1, paragraph 2 etc]}
    translated_processed = {} # store translated text {page: [translated paragraph 1, etc]}

    # Start of the input collection part of the program

    # get pdf file path from user, validates input
    valid_file_path = input_file()

    # ask user to choose translation engine, validateds input
    user_eng = user_chosen_eng()     

    # ask user if they want to see the supported languages for their chosen engine 
    answer = asks_see_supported(user_eng)
    if answer:
        open_supported_file(user_eng)

    # ask user target language, validates input
    user_lang, lang_name = user_chosen_lang(user_eng)

    # sum up to user all the info before doing processing
    print("Great, we are translating now " + valid_file_path + " to " + lang_name + ".\n")
    print("Preparing Bilingual pdf! This might take a bit =)\n")

    # start of processing

    # transform original pdf into 2 dict: original text, translated and count paragraphs per page    
    try: 
        source_processed, paragraphs = source_builder(valid_file_path)
        translated_processed = translator_builder (source_processed, user_lang, user_eng)
    except Exception:
        raise Exception ("Something unexpected happened! File could not be translated.")            
     

    # builds a new pdf with the table showing paragraph location, original text and translated
    header = "Translated to "+ lang_name.title() + " via " + user_eng.title()
    new_pdf (original = source_processed, translated = translated_processed , n_paragraphs = paragraphs , header_col3 = header)


    # opens bilingual pdf created
    print ("It worked! Go check =) \n")
    webbrowser.open("bilingual.pdf")

    # builds a json file for testing, commented since it's not necessary for end-user
    """
    with open('original.json', 'w', encoding = 'utf-8') as one:
        json.dump(source_processed, one, ensure_ascii = False, indent=4)
    with open('translated.json', 'w', encoding = 'utf-8') as two:
        json.dump(translated_processed, two, ensure_ascii = False, indent=4)

    """
                     



# FUNCTIONS

# ask user for PDF file path 
def input_file():        
    while True:
            try:
                file_path = input("Please insert the PDF file path to be translated: ")
                valid_file_path = check_file(file_path)  # check if file path and if is a valid PDF       
                return valid_file_path     
            except FileExistsError:
                print("Error loading the file, please check the file path or if file is a PDF.\n")
                pass

# test validy of PDF file/filepath 
def check_file(file_path):  
    file_path.strip()
    try: 
        doc = fitz.open(file_path)  # is it a readable file?
        return file_path
    except Exception:
        raise FileExistsError   

# ask user for search engine 
# PS: deepl is commented because translators library is having some API request issues
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

# ask user if they want to see supported languages for chosen engine 
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

# open PDF with supported languages according to chosen engine 
# PS: deepl is commented because translators library is having some API request issues
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

# ask user to input target language for translation 
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
        
# validate user lang input, and returns the language code accepted by translators libray
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
    
# extract texts from original pdf, populates them in a dictionary
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
                if sentence != False: # ignores blank paragraphs
                    # populating provisory lists in current page
                    provisional_original.append(sentence)                                 
                    n_par = n_par + 1
        
        # update list of number of paragraphs in each page
        p.append(n_par) 
        # builds dict with that page number as key and its list of paragraphs as values        
        original[n_page] = provisional_original        
        n_page = n_page + 1
    return original, p

# clean paragraphs of weird char, websites and string that contains no letters 
def p_cleaner(paragraph):  
    first_cleaning = re.sub(r"\n"," ", paragraph)
    first_cleaning = first_cleaning.replace("  ", " ").replace('\"',"'").strip() 

    if re.search(r"http|www", first_cleaning): # check if there is url and substitute for shorter "URL"
        second_cleaning = re.sub("http\S+","URL", first_cleaning)
        second_cleaning = re.sub("www\S+","URL", second_cleaning)

        check_sentence = second_cleaning.replace("URL", "1").strip() # gimmick to see if sentence will be just url + garbage
        final_sentence = second_cleaning
    else:
        check_sentence = first_cleaning
        final_sentence = first_cleaning


    for c in check_sentence: #checking if the sentence has just numbers, special char, url 
        if c.isalpha():
            check = True
            break
        else:
            check = False

    if check and final_sentence != "": # sentence has real words
        return final_sentence    
    else: # if it's a garbage sentence returns empty string
        return False    

# populates a dictionary with the translations
def translator_builder(original, lang, eng): 
    source = original 
    trans ={}   
    # go to each key and it's paragraphs and returns a dict with translation
    for page, paragraphs in source.items():
        provisory = []
        for i in paragraphs:
            new_sentence = translate(i, lang, eng)
            provisory.append(new_sentence)
        trans[page] = provisory 
    return trans  

# translate each paragraph    
def translate(paragraph, language, engine): 
    # uses google translate            
    try:
        translation = ts.translate_text(query_text = paragraph, translator = engine, from_language = 'auto', to_language=language)        
    except Exception:       
        translation = "ERROR: Could not translate, sorry!\n"
    return translation

# build new bilingual pdf
def new_pdf (original, translated, n_paragraphs, header_col3):
    # number total of paragraphs in the document
    total_para = sum (n_paragraphs)
    # create Document
    doc: Document = Document()
    # initial guess of how many rows will fit in a page
    max_rows_page = total_para 
    if max_rows_page > 12: # let's not guess too big
        max_rows_page = 12
    # try to create doc with table, if table is too big for page, max_rows_page degrease until it fits  
    while True:
        try:
            ct = 0 # keep count of paragraphs already added to the table
            t, l = create_new_table(doc, max_rows_page+1, header_col3) # creates first table and page, +1 for header 
            # starts to populate each paragraph in each already created row
            for page, paragraph in original.items():
                for index, para in enumerate(paragraph):        
                    col1 = str(page) + "." + str(index + 1) # +1 so first paragraph is 1 and not 0
                    col2 = para
                    col3 = translated[page][index]
                    t.add(Paragraph(col1)) # add localizor of the paragraph page.paragraph
                    t.add(Paragraph(col2)) # add original paragraph
                    t.add(Paragraph(col3)) # add translated paragraph
                    ct += 1 

                    # each time ct reaches a multiple of max_row: time to finish off the complete table/page and start new one
                    # unless we don't have many paragraphs, so no need for new page/table
                    if ct % max_rows_page == 0 and total_para > max_rows_page:
                        t.set_padding_on_all_cells(Decimal(3), Decimal(3), Decimal(3), Decimal(3))
                        l.add(t) # finish previous table and add to page
                        t, l = create_new_table(doc, max_rows_page+1, header_col3) # start new page and table
            
            # finish off last page
            t.set_padding_on_all_cells(Decimal(3), Decimal(3), Decimal(3), Decimal(3))
            l.add(t)

            # add finished doc with all stuff into a file
            with open("bilingual.pdf", "wb") as out_file_handle:
                PDF.dumps(out_file_handle, doc)
            break
        except Exception:
            # if max_rows_page was too big for a page, decreases it until fits
            max_rows_page += -1
            # reset the doc for next trial, otherwise it the max_row trials compoung in a doc
            doc: Document = Document() 

# create new page and table in the bilingual pdf
def create_new_table(doc, max_rows_page, header_col3):
    # create page object
    page: Page = Page()
    # add Page to Document
    doc.add_page(page)
    # set a PageLayout to stablish the "writable area"
    layout: PageLayout = SingleColumnLayout(page)
    # build Table that will go inside that area
    t: Table = FlexibleColumnWidthTable(number_of_columns=3, number_of_rows = max_rows_page)
    # add header on each page    
    t.add(Paragraph("Pg.par", font="Helvetica-Bold"))
    t.add(Paragraph("Original", font="Helvetica-Bold"))
    t.add(Paragraph(header_col3, font="Helvetica-Bold"))
    return t, layout 
    

if __name__ == "__main__":
    main()
