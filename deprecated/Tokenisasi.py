import xml.etree.ElementTree as ET
import collections

def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


def remove_notation(input_string):
    input_string = input_string[:-1] if input_string[-1] == '.' else input_string
    input_string = input_string[:-1] if input_string[-1] == '\"' else input_string
    input_string = input_string[:-1] if input_string[-1] == ',' else input_string
    input_string = input_string[1:] if input_string[0] == '\"' else input_string
    return input_string

if __name__ == "__main__":
    tree = ET.parse('6146.xml')
    root = tree.getroot()

    text_element = root[3]

    words = []
    for paragraph in text_element:
        lowered_text = paragraph.text.lower()
        splitted = lowered_text.split(' ')
        words += splitted

    token = {}
    for word in words:
        if not has_numbers(word):
            if token.has_key(remove_notation(word)):
                token[remove_notation(word)] += 1
            else:
                token[remove_notation(word)] = 1

    token_sorted = collections.OrderedDict(sorted(token.items()))
    print token_sorted.items()