def get_word_and_description(words):
    if not words:
        return None, None
    word_desc_pair = words.pop()
    return word_desc_pair['word'], word_desc_pair['description']

def create_hidden_word(word):
    return ['■' for _ in word]

def update_hidden_word(word, hidden_word, guess):
    for i, letter in enumerate(word):
        if letter.lower() == guess:
            hidden_word[i] = letter
    return hidden_word






