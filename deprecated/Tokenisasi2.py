import xml.etree.ElementTree as ET
import collections
import re
from os import listdir

def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


def isSentenceMark(input_string):
    return input_string in [',','.','\'','"','!', '@', '#', '$', '%', '-', '--']

def remove_notation(input_string):
    input_string = input_string[2:] if input_string[:2] == '--' else input_string
    input_string = input_string[:-1] if input_string[-1] == '.' else input_string
    input_string = input_string[:-1] if input_string[-1] == '\"' else input_string
    input_string = input_string[:-1] if input_string[-1] == ',' else input_string
    input_string = input_string[1:] if input_string[0] == '\"' else input_string
    return input_string


def find_text_pos(root_element):
    for element in root_element:
        if element.tag == "text":
            return element

if __name__ == "__main__":
    train_dir = "dataset/Training101"
    i = 1
    token = {}
    for xml in listdir(train_dir):
        if xml.endswith(".xml"):
            print i, "Processing", xml
            tree = ET.parse(train_dir+'/'+xml)
            root = tree.getroot()

            text_element = find_text_pos(root)

            words = []
            for paragraph in text_element:
                lowered_text = paragraph.text.lower()
                splitted = re.split(' |-|,',lowered_text)
                words += splitted
            for word in words:
                if not has_numbers(word) and not isSentenceMark(word) and len(word)>0:
                    try:
                        if token.has_key(remove_notation(word)):
                            token[remove_notation(word)] += 1

                        else:
                            token[remove_notation(word)] = 1
                    except Exception as e:
                        print e.message, word
            print i, "Finished", xml
            i+=1

    token_sorted = collections.OrderedDict(sorted(token.items()))
    output = open('output.txt', 'w')
    print 'Unique token =', len(token_sorted)
    print 'Find result in output.txt'
    output.write('Unique token = ' + str(len(token_sorted))+'\n')
    for unique in token_sorted.items():
        word = str(unique[0]) + ' = ' + str(unique[1])
        output.write(word)
        output.write('\n')
    # print token_sorted.items()
