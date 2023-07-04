import pytest
from bilingual_pdf import get_file, user_possible_lang
from rascunho import user_lang


def main():
    test_file_valid()
    test_user_possible_lang()
    test_user_lang()

# Test 1: test function that sees if user provided a valid pdf file and file path
def test_file_valid():
    assert (get_file('example1.pdf')) == True  # Valid pdf and valid file path
    with pytest.raises(ValueError):  # Not a pdf, but valid file path
        get_file("supported_languages.json")
    with pytest.raises(FileExistsError):  # Invalid file path
        get_file("nonexistent.pdf")
    with pytest.raises(FileExistsError):  # Corrupted pdf, valid file path
        get_file("corruptedpdf.pdf")

# Test 2: test language choosing
def test_user_possible_lang():
    assert (user_possible_lang('Y')) == True
    assert (user_possible_lang('y')) == True
    assert (user_possible_lang("Y ")) == True
    with pytest.raises(ValueError):  
        user_possible_lang("F")
    with pytest.raises(ValueError):  
        user_possible_lang("")
    with pytest.raises(ValueError):  
        user_possible_lang("yess")  

def test_user_lang(monkeypatch):
    inputs = ['English','english', 'en', 'Myanmar Burmese', 'Myanmar burmese', 'wrong', 'Zu', 'ZU']
    answers = ['en','en','en', 'my', 'my', None, 'zu', 'zu' ]
    for i in range(len(inputs)):
        monkeypatch.setattr('builtins.input', lambda _: inputs[i])
        result = user_lang()
        assert result == answers[i]
    
# Test 3: test text extraction
# Test 4: test pdf cleaners
# Test 5: test translation
# Test 6: test new pdf builder
if __name__ == "__main__":
    main()
