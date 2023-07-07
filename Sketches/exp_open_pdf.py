import webbrowser

def main():
    engine = "deepl"
    open_pdf_supported(engine)

def open_pdf_supported (engine):
    supported = {"google":"supported_google.pdf",
                 "deepl": "supported_deepl.pdf"}     
    if engine in supported:
        file = supported[engine]
        webbrowser.open(file) # Obvioylsy this doesnt work =(
    else:
        raise ValueError 


if __name__ == "__main__":
    main()