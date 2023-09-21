from _decimal import Decimal

from borb.pdf import PDF, Document, Page, FlexibleColumnWidthTable, Table, Paragraph, \
     PageLayout, SingleColumnLayout


original_text = {
    "1": [
        "5/8/23, 7:22 PM Politie schiet man dood bij huiszoeking in Gent: 'Hij richtte een wapen op agenten' | VRT NWS: nieuws",
        "B",
        "Aan de Franklin Rooseveltlaan in Gent, aan het Zuidpark, is een dode gevallen bij een schietincident tijdens een huiszoeking in een flatgebouw. Dat meldt het parket van Oost-Vlaanderen. 'De federale politie heeft de man neergeschoten toen hij een wapen richtte op de agenten.' Het gaat om de bewoner van het appartement die ook verdacht werd in een drugszaak.",
        "Radio 2, Ward Schouppe",
        "Update  17:17",
        "ij een huiszoeking in Gent heeft de federale politie deze ochtend een man van 44 doodgeschoten. Dat bevestigt het parket Oost-",
        "Vlaanderen. Het schietincident gebeurde rond 6 uur, in een flatgebouw aan de Franklin Rooseveltlaan, in de buurt van het Zuidpark.",
        "Politie schiet man dood bij huiszoeking in Gent: 'Hij richtte een wapen op agenten'",
        "Regio Regio",
        "Gent Gent"
    ],
    "2": [
        "5/8/23, 7:22 PM Politie schiet man dood bij huiszoeking in Gent: 'Hij richtte een wapen op agenten' | VRT NWS: nieuws",
        "De politie was er in het kader van een lopend drugsonderzoek. Toen de bewoner én verdachte een wapen richtte op de agenten, schoten ze hem neer. Er is nog geprobeerd om de man te reanimeren, maar dat is niet meer gelukt. Hij overleed later in het appartement. Het onderzoek loopt nu verder.   Het onderzoek zal moeten uitmaken of er sprake was van wettige zelfverdediging door de agent in kwestie. Bij het incident raakte niemand anders gewond. Er zijn momenteel geen aanwijzingen dat het geweld niet op een rechtsgeldige manier gebruikt werd of niet proportioneel was.",
        "Het onderzoek naar het door de politie gebruikte geweld is in handen van het Comité P. De speurders volgen de procedure zoals voorgeschreven in de omzendbrief over de afhandeling van de gevallen waarin de politiediensten zelf geweld gebruikten met de dood als gevolg. Dat houdt in dat de politieman niet van zijn vrijheid beroofd wordt of onmiddellijk verhoord wordt.",
        "BEKIJK - Caroline Verschuere van het Parket Oost-Vlaanderen legt uit hoe het onderzoek zal lopen:"
    ],
    "3": [
        "5/8/23, 7:22 PM Politie schiet man dood bij huiszoeking in Gent: 'Hij richtte een wapen op agenten' | VRT NWS: nieuws",
        "Beluister het meest recente regionieuws uit Oost-Vlaanderen",
        "1.0x"
    ]
}

translated_text = {
    "1": [
        "5/8/23, 7:22 pm Police shoots man killed during a search in Ghent: \"He pointed a weapon on agents\" | VRT NWS: News",
        "B",
        "On the Franklin Rooseveltlaan in Ghent, on the Zuidpark, a dead person fell at a shooting incident during a house search in an apartment building. The public prosecutor of East Flanders reports this. \"The federal police shot the man when he focused a weapon on the agents.\" It is about the occupant of the apartment who was also suspected in a drug shop.",
        "Radio 2, Ward Schouppe",
        "Update  17:17",
        "During a house search in Ghent, the federal police shot a man of 44 this morning. That confirms the public prosecutor's office",
        "Flanders. The shooting incident happened around 6 am, in an apartment building on Franklin Rooseveltlaan, near Zuidpark.",
        "Police shoots husband's house search in Ghent: \"He pointed a weapon at agents\"",
        "Regio Regio",
        "Gender"
    ],
    "2": [
        "5/8/23, 7:22 pm Police shoots man killed during a search in Ghent: \"He pointed a weapon on agents\" | VRT NWS: News",
        "The police were there in the context of an ongoing drug investigation. When the resident and the suspect pointed a weapon on the agents, they shot him down. An attempt has been made to resuscitate the man, but that was no longer successful. He died later in the apartment. The research is now continuing. The investigation will have to determine whether there was legal self -defense by the agent in question. Nobody else was injured in the incident. There are currently no indications that the violence was not used in a legally valid way or was not proportional.",
        "The investigation into the violence used by the police is in the hands of the P. Committee The Speurders follow the procedure as prescribed in the circular letter about the handling of the cases in which the police themselves used violence with death as a result. This means that the policeman is not deprived of his freedom or is immediately interrogated.",
        "View - Caroline Verschuere of the Public Prosecutor East Flanders explains how the research will go:"
    ],
    "3": [
        "5/8/23, 7:22 pm Police shoots man killed during a search in Ghent: \"He pointed a weapon on agents\" | VRT NWS: News",
        "Listen to the most recent regional news from East Flanders",
        "1.0"
    ]
}

list_para = [10,4,3]

def main():
    # create Document
    doc: Document = Document()
    max_rows_page = sum(list_para)
    
    # Add one row for header
    while True:
        try:
            ct = 0
            t, l = create_new_table(doc, max_rows_page+1)
            for page, paragraph in original_text.items():
                for index, para in enumerate(paragraph):        
                    col1 = str(page) + "." + str(index + 1)
                    col2 = para
                    col3 = translated_text[page][index]
                    t.add(Paragraph(col1))
                    t.add(Paragraph(col2))
                    t.add(Paragraph(col3))
                    ct += 1
                    #Need to add new page
                    if ct % max_rows_page == 0:
                        t.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
                        l.add(t)
                        t, l = create_new_table(doc, max_rows_page+1)
            t.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
            l.add(t)
            with open("output.pdf", "wb") as out_file_handle:
                PDF.dumps(out_file_handle, doc)
            break
        except Exception as what:
            max_rows_page += -1
            doc: Document = Document()
            print (what)
            
            
def create_new_table(doc, max_rows_page):
    page: Page = Page()
    # add Page to Document
    doc.add_page(page)
    # set a PageLayout
    layout: PageLayout = SingleColumnLayout(page)
    # build Table
    t: Table = FlexibleColumnWidthTable(number_of_columns=3, number_of_rows=max_rows_page)    
    t.add(Paragraph("Pag.Par", font="Helvetica-Bold"))
    t.add(Paragraph("Original", font="Helvetica-Bold"))
    t.add(Paragraph("Translated", font="Helvetica-Bold"))
    return t, layout

"""def add_row(original, translated, t):
        for page in original.keys():
            for para in original[page]:        
                first_col = para
                num_par = original[page].index(para)        
                second_col= translated[page][num_par]
                page_paragraph = str(page)+"."+str(num_par+1)
                t.add(Paragraph(page_paragraph)) 
                t.add(Paragraph(first_col))
                t.add(Paragraph(second_col)) 
                original.pop(page[num_par])
                translated.pop(page[num_par])

                break"""


"""    for page in range(1,n_pages+1):
        page: Page = Page()
        # add Page to Document
        doc.add_page(page)
        # set a PageLayout
        layout: PageLayout = SingleColumnLayout(page)
        # build Table
        t: Table = FlexibleColumnWidthTable(number_of_columns=3, number_of_rows=max_rows_page)
        #header
        t.add(Paragraph("Pag.Par", font="Helvetica-Bold"))
        t.add(Paragraph("Original", font="Helvetica-Bold"))
        t.add(Paragraph("Translated", font="Helvetica-Bold"))
        for row in range(1, max_rows_page):
            add_row(col1, original_text[index], translated_text[index], t)
            #add_row(original_text, translated_text, t)
                             
        t.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
        layout.add(t)
    # store
    with open("output.pdf", "wb") as out_file_handle:
        PDF.dumps(out_file_handle, doc)"""


if __name__ == "__main__":
    main()