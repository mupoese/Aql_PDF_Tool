from langdetect import detect

def detect_language(text):
    return detect(text)

def word_by_word_check(text):
    words = text.split()
    for word in words:
        # Voeg hier taalvalidatie of correctie toe
        pass
