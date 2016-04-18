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


def get_all_text(files_dir):
    text_list = list()
    for xml in listdir(files_dir):
        if xml.endswith(".xml"):
            print xml
            tree = ET.parse(files_dir+'/'+xml)
            root = tree.getroot()
            text_list.append(find_text_pos(root))
    return text_list


def get_text_counter(elements):
    doc_lists = list()
    stemmer = LancasterStemmer()
    for element in elements:
        words = []
        for paragraph in element:
            lowered_text = paragraph.text.lower()
            lowered_text = re.sub(regex_char, ' ', lowered_text)
            splits = re.split(' ', lowered_text)
            words += [stemmer.stem(item) for item in splits]
        word_counter = Counter(words)
        word_counter.pop('')
        doc_lists.append(word_counter)
    return doc_lists


def get_doc_freq(counters):
    token_from_all = Counter()
    for counter in counters:
        temp = counter.copy()
        for key in temp:
            temp[key] = 1
        token_from_all += temp
    return token_from_all


if __name__ == "__main__":
    train_dir = "dataset/Training101"
    text_elements = get_all_text(train_dir)
    token_counters = get_text_counter(text_elements)

    term_doc_freq = get_doc_freq(token_counters)
    term_all_docs = sorted(term_doc_freq.keys())

    print term_doc_freq
    print term_all_docs
