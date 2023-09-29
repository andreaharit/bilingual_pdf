import re




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
    
def main():
    sentence = '  \n'
    answer = p_cleaner (sentence)
    print (answer)

if __name__ == "__main__":
  main()
