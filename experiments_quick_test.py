original = {
  1: ["ford", "citroen"],
  2: ["mustang", "carro"],
  3: ["1941"]
}
translated = {
     1: ["FORDA", "CITRUNA"],
  2: ["MUSTANGA", "CARRA"],
  3: ["XXXX"]
}

provisory_list =[]

for (k1, p1), (k2,p2) in zip(original.items(), translated.items()):
    page_paragraph =""    
    for (i,j) in zip(p1,p2):
        num_par = p1.index(i)
        page_paragraph = str(k1)+"."+str(num_par+1)
        first_col = i
        second_col = j
        provisory_list.append([page_paragraph, first_col, second_col])

print(provisory_list)


"""for page, paragraph in original.items():
    for index, para in enumerate(paragraph):        
        col1 = str(page) + "." + str(index + 1)
        col2 = para
        col3 = translated[page][index]
        num_par = original[page].index(para)        
        second_col= translated[page][num_par]
        page_paragraph = str(page)+"."+str(num_par)
        print(page_paragraph + ": " + first_col + "  //  " + second_col)"""