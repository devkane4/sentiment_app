from janome.tokenizer import Tokenizer

t = Tokenizer()

def tokenize(text):
    return [token.surface for token in t.tokenize(text)]

def mecab_tokenizer(text):
    return [token.surface for token in t.tokenize(text)]