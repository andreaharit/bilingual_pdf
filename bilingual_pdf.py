import webbrowser
import re
import json
import warnings

import fitz # pdf parser
import translators as ts # translation library
from _decimal import Decimal # supporting library for borb, regarding sizing
from borb.pdf import PDF, Document, Page, FlexibleColumnWidthTable, Table, Paragraph, \
     PageLayout, SingleColumnLayout # creates new pdf with tables



""" This is a translation program that from user via terminal: a pdf filapath, language and engine.
    And it builts a new pdf that contains a table where each row is a paragraph of the original PDF.
    And each column:
        - The number of page and paragraph ex 2.1 is the first paragraph if the second page.
        - The original text.
        - The translated text.
    It is a pet project of someone who is learning Python, and doesn't know OOP yet. 
    And it was submeted on the EDX course CS50P as a final project.
    This version was finished on 29/09/2023 by Andrea Haritçalde.
"""

def main():
    # filters leftover debug warning from translators library, forgotten by the developer
    warnings.filterwarnings('ignore')

    # initiates variables
    source_processed = {} # store original text {page: [paragraph 1, paragraph 2 etc]}
    translated_processed = {} # store translated text {page: [translated paragraph 1, etc]}

    # start of the input collection part of the program

    # gets pdf file path from user, validates input
    valid_file_path = input_file()

    # asks user to choose translation engine, validateds input
    user_eng = user_chosen_eng()

    # asks user if they want to see the supported languages for their chosen engine
    answer = asks_see_supported()
    if answer:
        open_supported_file(user_eng)

    # asks user target language, validates input
    user_lang, lang_name = user_chosen_lang(user_eng)

    # sum up to user all the info before doing processing
    print("Great, we are translating now " + valid_file_path + " to " + lang_name + ".\n")
    print("Preparing Bilingual pdf! This might take a bit =)\n")

    # start of processing
    # transforms original pdf into 2 dict: original text, translated and count paragraphs per page
    try:
        source_processed, paragraphs = source_builder(valid_file_path)
        translated_processed = translator_builder (source_processed, user_lang, user_eng)
    except Exception:
        raise Exception ("Something unexpected happened! File could not be translated.")

    # builds a new pdf with the table showing paragraph location, original text and translated
    header = "Translated to " + lang_name.title() + " via " + user_eng.title()
    new_pdf (original = source_processed, translated = translated_processed,
             n_paragraphs = paragraphs, header_col3 = header)

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

# asks user for PDF file path
# returns filepath as str if is valid input, or reprompt user if invalid
def input_file():
    
    while True:
        try:
            file_path = input("Please insert the PDF file path to be translated: ")
            valid_file_path = check_file(file_path)  # check if file path and if is a valid PDF
            return valid_file_path
        except FileExistsError:
            print("Error loading the file, please check the file path or if file is a PDF.\n")
            pass

# tests validy of PDF file/filepath
# returns filepath as str if arg is valid, or error if invalid
def check_file(file_path):
    file_path.strip()
    try:
        doc = fitz.open(file_path)  # is it a readable file?
        return file_path
    except Exception:
        raise FileExistsError

# asks user for search engine
# returns engine as str if input is valid, or reprompt user if invalid
# PS: deepl is commented because translators library is having some API request issues
def user_chosen_eng():
    engines = {
        "g": "google",
        "b": "bing"
        # "d": "deepl"
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

# asks user if they want to see supported languages for chosen engine
# returns bool for y/n answer if input is valid, or reprompts user if invalid
def asks_see_supported(arg= None): # arg is a quickfix for monkeypatch on unit_test
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

# opens in user's app a PDF with supported languages according to chosen engine
# raises error if there was a problem opening this PDF
# PS: deepl is commented because translators library is having some API request issues
def open_supported_file(engine = "google"):
    supported = {"google": "supported_google.pdf",
                 "bing": "supported_bing.pdf"                 
                 #"deepl": "supported_deepl.pdf"
                 }
    if engine in supported:
        file = supported[engine]
        webbrowser.open(file)
        return True # not sure if this is necessary, TO DO
    else:
        raise ValueError

# asks user to input target language for translation
# returns language code (ex: en, fr) and name (ex: english, french) if input is valid
# or loop user if invalid
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

# validates user lang input
# returns language code (ex: en, fr) and name (english french) if arg is supportd by engine
# or raise error if arg is not supported
def validadate_lang(user_lang, engine = "google"):
    eng_files = {"google": "supported_google.json",
                 "bing": "supported_bing.json"
                 #"deepl": "supported_deepl.json"
                 }

    # loads supported languages according to chosen engine
    try:
        f = open(eng_files[engine]) # opens the json with supported languages for given engine
        supported =  json.load(f)
    except Exception:
        raise ImportError

    # sees if user input is supported by the engine
    try:
        if user_lang in supported.keys(): # user typed alredy the language code? ex "en"
            lang_code = user_lang
        else: # user typed the long version? ex "English"
            for code, names in supported.items():
                if type(names) is not list: # if there is just one name for the lang (some langs have many)
                    names = [names] # tuns into list, next line checks for langs with one or multiple names
                if user_lang in names:  # then checks names in lists for match with user input
                    lang_code = code

        # getting language in full name to print to user
        if type(supported[lang_code]) is not list:
            language = supported[lang_code] # user typed code, language has only one way of naming
        else:
            language = supported[lang_code][0] # user typed code, language has many names

        f.close()
        return lang_code, language
    except Exception:
        raise ValueError

# extracts texts from original pdf
# returns dict with original text and list counting paragraphs per page
def source_builder(document):
    # variables initialization
    n_page = 1  # page counter, starts in 1 to be user friendlier
    p = [] # stores number of paragraphs per page


    # dicts to hold original: key is page's number, elements are its paragraphs
    original = {}

    # opens, reads and populates dictionary
    doc = fitz.open(document)

    for page in doc:
        provisional_original = [] # provisory list of paragraphs for each page
        n_par = 0 # provisory counter of number of paragraph for each page

        # reads each "block" in the page, see PyMuPDF documentation
        source = page.get_text("blocks")
        for paragraph in source:
            if paragraph[6] == 0:  # ignores blocks that are type "image"
                sentence = p_cleaner(paragraph[4]) # cleans weird chars or paragraphs
                if sentence is not False: # ignores blank paragraphs
                    # populating provisory lists in current page
                    provisional_original.append(sentence)
                    n_par += 1

        # updates list of number of paragraphs in each page
        p.append(n_par)
        # builds dict with that page number as key and its list of paragraphs as values
        original[n_page] = provisional_original
        n_page += 1
    return original, p

# cleans paragraphs of weird char, websites and string that contains no letters
# returns cleaned paragraph as str
def p_cleaner(paragraph):
    check = False
    
    first_cleaning = re.sub(r"\n"," ", paragraph)
    first_cleaning = first_cleaning.replace("  ", " ").replace('\"',"'").strip()

    if re.search(r"http|www", first_cleaning): # check if there is url and substitute for shorter "URL"
        second_cleaning = re.sub(r"http\S+","URL", first_cleaning)
        second_cleaning = re.sub(r"www\S+","URL", second_cleaning)

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

# builds and returns dictionary with the translations
def translator_builder(original, lang, eng):
    source = original
    trans = {}
    # go to each key and it's paragraphs and returns a dict with translation
    for page, paragraphs in source.items():
        provisory = []
        for i in paragraphs:
            new_sentence = translate(i, lang, eng)
            provisory.append(new_sentence)
        trans[page] = provisory
    return trans

# translates and returns paragraph as str
def translate (paragraph, language, engine):
    # uses google translate
    try:
        translation = ts.translate_text(query_text = paragraph,
                                        translator = engine,
                                        from_language = 'auto',
                                        to_language=language)
    except Exception:
        translation = "ERROR: Could not translate, sorry!\n"
    return translation

# builds new bilingual pdf
# opens document in user's default pdf app
def new_pdf (original, translated, n_paragraphs, header_col3):
    # number total of paragraphs in the document
    total_para = sum (n_paragraphs)
    # create Document
    doc: Document = Document()
    # initial guess of how many rows will fit in a page
    max_rows_page = total_para
    if max_rows_page > 12: # let's not guess too big
        max_rows_page = 12
    # tries to create doc with table, if table is too big, max_rows_page degrease until it fits
    while True:
        try:
            count = 0 # keep count of paragraphs already added to the table
            t, l = create_new_table(doc, max_rows_page+1, header_col3) # creates first table/page, +1 for header
            # starts to populate each paragraph in each already created row
            for page, paragraph in original.items():
                for index, para in enumerate(paragraph):
                    col1 = str(page) + "." + str(index + 1) # +1 so first paragraph is 1 and not 0
                    col2 = para
                    col3 = translated[page][index]
                    t.add(Paragraph(col1)) # add localizor of the paragraph page.paragraph
                    t.add(Paragraph(col2)) # add original paragraph
                    t.add(Paragraph(col3)) # add translated paragraph
                    count += 1

                    # each time counter reaches a multiple of max_row:
                    # time to finish off the complete table/page and start new one
                    # unless we don't have many paragraphs, so no need for new page/table
                    if count % max_rows_page == 0 and total_para > max_rows_page:
                        t.set_padding_on_all_cells(Decimal(3), Decimal(3), Decimal(3), Decimal(3))
                        l.add(t) # finish previous table and add to page
                        t, l = create_new_table(doc, max_rows_page+1, header_col3) # start new page + table

            # finishes off last page
            t.set_padding_on_all_cells(Decimal(3), Decimal(3), Decimal(3), Decimal(3))
            l.add(t)

            # adds finished doc with all stuff into a file
            with open("bilingual.pdf", "wb") as out_file_handle:
                PDF.dumps(out_file_handle, doc)
            break
        except Exception:
            # if max_rows_page was too big for a page, decreases it until fits
            max_rows_page -= 1
            # resets the doc for next trial
            doc: Document = Document()

# creates new page and table in the bilingual pdf
# returns empty table and page objects
def create_new_table(doc, max_rows_page, header_col3):
    # creates page object
    page: Page = Page()
    # adds Page to Document
    doc.add_page(page)
    # sets a PageLayout to stablish the "writable area"
    layout: PageLayout = SingleColumnLayout(page)
    # builds Table that will go inside that area
    t: Table = FlexibleColumnWidthTable(number_of_columns=3, number_of_rows = max_rows_page)
    # adds header on each page
    t.add(Paragraph("Pg.par", font="Helvetica-Bold"))
    t.add(Paragraph("Original", font="Helvetica-Bold"))
    t.add(Paragraph(header_col3, font="Helvetica-Bold"))
    return t, layout

if __name__ == "__main__":
    main()
