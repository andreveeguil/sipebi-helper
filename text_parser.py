import re
import json

class Sentence:
    is_commma = False
    is_fullstop = False
    is_question = False
    is_exclamation = False

    def __init__(self, sentence, is_fullstop=False, is_question=False, is_exclamation=False):
        self.sentence = sentence
        self.is_fullstop = is_fullstop
        self.is_question = is_question
        self.is_exclamation = is_exclamation

    def __repr__(self):
        return f"Sentence: Fullstop: {self.is_fullstop}, Question: {self.is_question}, Exclamation: {self.is_exclamation}"

    def __str(self):
        return f"Sentence: Fullstop: {self.is_fullstop}, Question: {self.is_question}, Exclamation: {self.is_exclamation}"

# Opening file and getting text
text = None
with open("testing.txt") as f:
    text = f.read()

# Split the text into sentence
sentences = []
sentence_objects = []
separated_text = text.split('"')
for text_piece in separated_text:
    text_piece_separated = re.split("\.|\?|!", text_piece)
    match_order = re.findall("(\.)|(\?)|(!)", text_piece)
    for i, match in enumerate(match_order):
        if match[0] == ".":
            sentence = Sentence(text_piece_separated[i], is_fullstop=True)
        elif match[1] == "?":
            sentence = Sentence(text_piece_separated[i], is_question=True)
        elif match[2] == "!":
            sentence = Sentence(text_piece_separated[i], is_exclamation=True)
        sentence_objects.append(sentence)
    sentences.extend(text_piece_separated)

sentences = [sentence.strip() for sentence in sentences]
sentences = [sentence.lower() for sentence in sentences if sentence]
# Classify the sentence into attributes

# Create a matrix to count the occurence of two words together
word_matrix = {}
word_counter = {}
for sentence in sentences:
    words = sentence.split(" ")
    for word in words:
        word_counter[word] = word_counter.get(word, 0) + 1
        word_matrix[word] = {}

    for i in range(len(words)):
        for j in range(i+1, len(words)):
            word_matrix[words[i]][words[j]] = word_matrix[words[i]].get(words[j], 0) + 1
            word_matrix[words[j]][words[i]] = word_matrix[words[j]].get(words[i], 0) + 1

with open("word_matrix.json", "w") as f:
    f.write(json.dumps(word_matrix))

with open("word_counter.json", "w") as f:
    f.write(json.dumps(word_counter))

for sentence in sentence_objects:
    print(sentence)
