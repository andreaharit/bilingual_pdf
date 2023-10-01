# Bilingual_PDF

## What it does

Bilingual_PDF is a Python program that asks the user for a PDF document, a target language for translation, and outputs a new PDF where you can compare the original text and the translated one, paragraph per paragraph.

The new PDF has a table where each row is a paragraph. And the three columns are:

- **Page/Paragraph**. This is a numeric ID of the page and paragraph. Example: 1.1 is the first page and its first paragraph.
- **Original**. The original text.
- **Translated**. The translated text.

This program does not recognize image-texts, but as long as the text is selectable in the original PDF it should try to translate it.
The program was tested with kid's books, plain text PDFs, and PDFs printed from websites.

By no means it is perfect, this is a beginner's pet-project.

## Motivation

I am learning a new language myself, and often using translating websites (Google, Bing, Deepl) with a lot of text can get quite confusing. You see a wall of translated text and it's hard to see which paragraph is the translation of which. Also, you can't save the translation easily.

Furthermore, this program was submitted as a final project for the course [Harvard (CS50P) on EDx](https://cs50.harvard.edu/python/2022/).

## Libraries used and versions

- [PyMuPDF](https://pymupdf.readthedocs.io/) is used to extract the text from the original PDF.
- [Translators](https://pypi.org/project/translators/) is used to translate the text.
- [Borb](https://github.com/jorisschellekens/borb) is used to build the new bilingual PDF.

The dependencies are in the requirements.txt.

## Files in this project

### Required to run the program:

- _bilingual_pdf.py_ is where all the code is.
- the jsons contain the supported languages for each translation engine. It's used to check for the validity of the user's input and get the accepted language code for the translators library.
- the pdfs contain the supported languagues for each engine, and will be opened during the program if the user wants to see this info.

OBS: since Deepl is having issues in the translators library, its json and pdf area also no required.

### Not required to run the program:

- The Unit test directory contains the unit tests code for some functions in the program. It requires to work the file example1.pdf for one of the tests.
- Many commits may have files with names as "experiments", "sketches". Those were files used as a thinking place to build funcions without messing with the main code.

## How to use it

After running the program in your IDE of choice, the program asks the user in the **terminal** for the following inputs:

- The PDF's file path to be translated.
- Which translation engine the user wants to use.
- If the user wants to see the supported languages they can choose from for that engine (Y/N answer). If yes, it opens a pdf with the info.
- The target language for translation.

And finally, it spits the new bilingual PDF and opens it to the user.

So far the engines supported are Google and Bing. The languague each one support are in the ones pointed out in the translators documentation.

## Important observations

- Sometimes the program doesn't do a perfect job depending on how the paragraphs were splitted in the original doc.
- This is a **beginner's program**. If it burns your eyes seeing my code, I am sorry and I'd appreciate any polite feedback.
- I don't know OOP _yet_. Nor how to make packages. So it's all in one file.
- Deepl is commented as an option because the library Translators was having an issue with it.
- There is much to improve in terms of cleaning relevant text (as repetitive texts from headers and footers for example)
- It looks like Borb will soon release a version that solves the issue of having to calculate by hand how big a table can be in the pages, until them, the way it was done in the program is not perfect (blank pages at the end, or blank table/cells at the end), but it searves its purpose

## What can be improved besides the beginner's code stuff

The priotity:

- Better cleaning of irrelevant texts.
- Wait for Borb to release new version of how to fit a huge table in multiple pages that will then be created automatically, or improve this program solution.
- Wait for Deepl to work again, or do a work around without the translators library

The next-level stuff:

- Recognize image-texts.
- Give more options for sources to be translated: webpages, and other file formats.
- Give more options for file output.

<details>
  <summary>Personal journey</summary>

### What I learned

- I learned a lot about reading documentation, even though 99.99% of all documentation is still very "over 1000 IQ" cryptic to me.
- I learned about unit tests, specially monkeypatch (it took a while to figure this one out).
- My Googleing skills and "let's-adapt-this-stack-overflow-answer" are a lot better.
- I learned a bit about libraries for text extraction and PDF manipulation.
- I started using git.

### What is still on my mind

- I wonder if there was a non-complex (imo) way of outputting the table into a pdf that is not only using borb. Where the text is selectable.
- I wonder if using the webbrowser library is a good way of opening a pdf. I had to set by hand the required pdfs to read-only, because it was easier, but this feels wrong.
- I need to learn how to reference stuff between directories. I mean, CS50 asks to put all in the same directory, but how should I do it if it wasn't the case. No idea.
- I still struggle to know when I am making a function too big and doing too much stuff.
- As much as I wonder what is the balance between commenting for me or for others.
- Sometimes we commit to a way of organizing the data that later we discover that is a pain in the ass, like organizing the dictionaries like I did { page: [list of paragraphs]},just because I wanted to keep track of the location of each paragraph. In conversations with my partner he argued there were better ways. But now a lot is done, and redoing it is so much more work. And so goes life.
- Also seeing that Borb might do the same as PyMuPDF to extract text, but then again, you are already commited. How bad it is to use two libraries when maybe just one was necessary?
- I need to learn OOP. I have a feeling there is a lot of repetition and organization problems that would work better with OOP.

</details>
