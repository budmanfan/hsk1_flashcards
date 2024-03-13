import json

with open("hsk1_vocab.json", 'r', encoding='utf-8') as file:
    vocab_data = json.load(file)
    
print(vocab_data['0'])
