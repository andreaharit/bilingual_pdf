teste={
        1:["oi","tudo bem", "a","b","c","d","tchau"],
        2:["oi","tudo bem", "e","f","g","h","tchau"],
        3:["oi","tudo", "i","j","k","tchau"],
        4:["oi","tudo bem", "i", "l","m","n","o","p","q"],
        5:["oi","tudo bem"],
    }

    hf_cleaner(teste)

def hf_cleaner(original_dict): # TO DO clean dictionary with original from repetitive phrases that might be footers and headers
    to_clean = original_dict
    
    i = 1
      
    size_page = len(to_clean)    
    
    while  i <= size_page:
        j = 0
        size_first = len(to_clean[i])
        size_second = len (to_clean[i+1])        
        while j < min(size_first, size_second):
            first_element = to_clean[i][j] 
            second_element = to_clean[i+1][j]
            if first_element == second_element :
                repetido = first_element
                print(f" palavra repetida é {repetido}\n")
                print(f"paginas sao  {i}, {i+1}, item {j}\n")
                
            else: 

                diferente = first_element
                diferente2 = second_element
                print (f"item nao é repetido:  {diferente} versus {diferente2}\n") 
                break             
            j += 1  
            print("--------")   
        i += 1
        print("XXXXXXXXXXX")  
                
                

        

    
         





    doc = source_builder("example3.pdf")
    # builds a json file
    with open('clean_original6.json', 'w', encoding = 'utf-8') as out_file:
        json.dump(doc, out_file, ensure_ascii = False, indent=4)

    



