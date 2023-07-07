import pytest
from bilingual_pdf  import check_file, user_chosen_eng, asks_see_supported, validadate_lang


def main():
    
    test_file_valid()
    test_chosen_eng()
    test_supoported_pdf()
    test_validadate_lang()

# Test 1: test if user provided a valid pdf file and file path
def test_file_valid():
    
    assert (check_file('example1.pdf')) == 'example1.pdf'  # Valid pdf and valid file path
    with pytest.raises(FileExistsError):  # Not a pdf, but valid file path
        check_file("supported_languages.json")
    with pytest.raises(FileExistsError):  # Invalid file path
        check_file("nonexistent.pdf")
    with pytest.raises(FileExistsError):  # Corrupted pdf, valid file path
        check_file("corruptedpdf.pdf")

# Teste 2: test choice of engine
def test_chosen_eng(monkeypatch):
    inputs = ['google','Google', 'g', 'G',"deepl", "d"]
   
    for i in inputs[0:4]:    
        monkeypatch.setattr('builtins.input', lambda _: i)
        result = user_chosen_eng()
        assert result == "google"
       
    for j in inputs[4:]:
        monkeypatch.setattr('builtins.input', lambda _: j)
        result = user_chosen_eng()
        assert result == "deepl"
    


# Test 3: test if user wants to see the supported languagues
def test_supoported_pdf(monkeypatch):
    inputs = ["Y", "y ","n"]
    expected= [True, True, False]
    for i in range(len(inputs)):
        monkeypatch.setattr('builtins.input', lambda _: inputs[i])       
        result = asks_see_supported("google")
        assert result == expected[i]
    
# Test 4: test if languague is accepted by engine and code return
def test_validadate_lang(): 
    inputs = ['English','english', 'en', 'Myanmar Burmese', 'Myanmar burmese',  'zu']
    answers = ['en','en','en', 'my', 'my', 'zu' ]  
    for i in range(len(inputs)):      
        assert (validadate_lang(inputs[i], "google")) == answers[i] 
    for eng in ["google","deepl"]:
        with pytest.raises (ValueError):
            validadate_lang("blah", eng)
    for j in range(3): 
        assert (validadate_lang(inputs[j], "deepl")) == answers[j] 



    

     


    
# Test 3: test text extraction
# Test 4: test pdf cleaners
# Test 5: test translation
# Test 6: test new pdf builder


if __name__ == "__main__":
    main()
