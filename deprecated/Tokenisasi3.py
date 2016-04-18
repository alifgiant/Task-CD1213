import xml.etree.ElementTree as ET
import re
import json
from collections import Counter
from os import listdir
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer


regex_char = '[/.,\'"$()0-9!?@#%^&*;\\|<>+_:=-]'


def find_text_pos(root_element):
    for element in root_element:
        if element.tag == "text":
            return element

if __name__ == "__main__":
    train_dir = "dataset/Training101"
    i = 1
    token = {}
    output = open('output.txt', 'w')
    for xml in listdir(train_dir):
        if xml.endswith(".xml"):
            print i, "Processing", xml
            tree = ET.parse(train_dir+'/'+xml)
            root = tree.getroot()

            text_element = find_text_pos(root)

            words = []
            for paragraph in text_element:
                lowered_text = paragraph.text.lower()
                lowered_text = re.sub(regex_char, ' ', lowered_text)
                splitted = re.split(' ', lowered_text)
                words += splitted

            print i, "Finished", xml
            i+=1
            unique_origin_word_counter = Counter(words)
            unique_origin_word_counter.pop('')

            lemma = WordNetLemmatizer()
            unique_lemmatize_word_counter = Counter([lemma.lemmatize(item) for item in words])
            unique_lemmatize_word_counter.pop('')
            # print unique_origin_word_counter.items()

            stemmer = LancasterStemmer()
            unique_stemmed_word_counter = Counter([stemmer.stem(item) for item in words])
            unique_stemmed_word_counter.pop('')
            # print unique_stemmed_word_counter.items()

            output.write('-------------TF------------')
            output.write('\nFILE '+xml+' origin word: ')
            output.write(json.dumps(unique_origin_word_counter.items()))
            output.write('\nFILE '+xml+' lemmatize word: ')
            output.write(json.dumps(unique_lemmatize_word_counter.items()))
            output.write('\nFILE '+xml+' stemmed word: ')
            output.write(json.dumps(unique_stemmed_word_counter.items()))
            output.write('\n')