# This work is still in progress

# Bilingual pdf builder
## What it does
Bilingual PDF builder is a Python program that asks the user for a PDF document, a target language for translation, and outputs a new PDF where you can compare the original text and the translated one, paragraph per paragraph.

The new PDF has a table where each row is a paragraph. And the three columns are: 
- **Index**. This is a numeric ID of the page and paragraph. Example: 1.1 is the first page and its first paragraph.
- **Original**. The original text.
- **Translated**. The translated text.

This program does not recognize image-texts, but as long as the text is selectable in the original PDF it should try to translate it.
The program was tested with kid's books, plain text PDFs, and PDFs printed from websites. 

## Motivation

I am learning a new language myself, and often using translating websites (Google, Deepl) with a lot of text can get quite confusing. You see a wall of translated text and it's hard to see which paragraph is the translation of which. Also, you can't save the translation easily. 

Furthermore, this program was submitted as a final project for the course [Harvard (CS50P) on EDx](https://cs50.harvard.edu/python/2022/). 

## Libraries used and versions
- [PyMuPDF 1.22.2](https://pymupdf.readthedocs.io/)
- [Translators 5.7.1](https://pypi.org/project/translators/)
- [Matplotlib 3.7.1](https://matplotlib.org/)

PyMuPDF was used to extract the text from the original PDF. Translators to translate the original text. Matplotlib to output the table into the new PDF. Other dependencies are in the requirements.txt. 

## Files in this project
### Required to run the program:
- _bilingual_pdf.py_ is where all the code is.
- the jsons contain the supported languages for each translation engine. It's used to check for the validity of the user's input and get the accepted language code for the translators library.
- the pdfs contain the supported languagues for each engine, and will be opened during the program if the user wants to see this info.
 
### Not required to run the program:
- The Unit test directory contains the unit tests code and the files necessary to run the tests. I would like to point out the some files are a duplicate because I don't know how yet how to open some stuff by reference yet.
- The Sketches directory contains files I am using to keep track of experiments for some functions. Also you might see duplicated files there for the same reason as above.

## How to use it
After running the program in your IDE of choice, the program asks the user in the **terminal** for the following inputs:
- The PDF's file path to be translated.
- If the user wants to see the supported languages they can choose from (Y/N answer). If yes, it opens a pdf with the info.
- Which translation engine the user wants to use (Google, Deepl).
- Where the user wants to save the new PDF and its name. (TO DO)
  
And finally, it spits the new bilingual PDF. (TO DO)

## Important observations
- Sometimes the program doesn't do a perfect job depending on how the paragraphs were splitted in the original doc.
- This is a **beginner's program**. If it burns your eyes seeing my code, I am sorry and I'd appreciate any polite feedback.
- I don't know OOP _yet_.


## What can be improved besides the beginner's code stuff
- Build a simple GUI so things aren't done via terminal.
- Recognize image-texts.
- Give more options for sources to be translated: webpages, and other file formats.
- Give more options for file output.
- Make it possible to compare different translations from different engines.


<details>
  <summary>## Personal journey</summary>

### What I learned
- I learned a lot about reading documentation, even though 99.99% of all documentation is still very "over 1000 IQ" cryptic to me.
- I learned about unit tests, specially monkeypatch (it took a while to figure this one out).
- My Googleing skills and "let's-adapt-this-stack-overflow-answer" are a lot better.
- I learned a bit about libraries for text extraction and PDF manipulation.
- I started using git.

### What is still on my mind
- I wonder if there was a non-complex (imo) way of outputting the table using only PyMuPDF, or if it was ok to use another library (MatPlotLib) just because it was easier for me to figure that one out.
- I wonder if I should delete the checking for extension and if the file path is valid. Since all that matters is if the file is readable.
- I wonder if using the webbrowser library is a good way of opening a pdf. I had to set by hand the pdfs to read-only, because it was easier, but this feels wrong.
- I need to learn how to reference stuff between directories. I mean, running the unit test code from its directory gave a lot of errors because (so I learned) many stuff work in reference of the current work directory.
- I wonder if it's better to put the user input questions in the main or inside functions as I did.
- I wonder if I should separate stuff in different files instead of one with all the functions and main together.
- I wonder what is the balance between commenting for me or for others.
- I need to learn OOP.
</details>
