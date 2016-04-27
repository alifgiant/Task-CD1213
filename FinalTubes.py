import xml.etree.ElementTree as ET
import re
import json
from sklearn import svm, metrics, neighbors, naive_bayes
from collections import Counter, OrderedDict
from os import listdir
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
import file_reader
import os.path
import numpy as np


regex_char = '[^a-zA-Z\s]|^\w'


def find_text_pos(root_element):
    for element in root_element:
        if element.tag == "text":
            return element


def get_all_text(files_dir):
    text_dic = dict()
    for xml in listdir(files_dir):
        if xml.endswith(".xml"):
            tree = ET.parse(files_dir+'/'+xml)
            root = tree.getroot()
            text_dic[int(xml.title()[:-4])] = find_text_pos(root)
    text_dic = OrderedDict(sorted(text_dic.items()))
    # print text_dic.keys()
    return text_dic.values()


def get_text_counter(elements):
    doc_lists = list()
    stemmer = LancasterStemmer()
    for element in elements:
        words = []
        for paragraph in element:
            lowered_text = paragraph.text.lower()
            regex = re.compile(regex_char)
            lowered_text = regex.sub('', lowered_text)
            # lowered_text = re.sub(regex_char, ' ', lowered_text)
            splits = re.split(' ', lowered_text)
            words += [stemmer.stem(item) for item in splits if item not in stopwords.words('english')]
        word_counter = Counter(words)
        if '' in word_counter:
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


def get_feature_training(doc_freq, all_terms, counters):
    from math import log10
    return [[((0 if counter[term] == 0 else 1+log10(counter[term])) *
             0 if doc_freq[term] == 0 else log10(len(counters)/float(doc_freq[term])))
             for term in all_terms] for counter in counters]


if __name__ == "__main__":
    # training
    if not os.path.isfile('training_result.txt'):
        train_dir = "dataset/Training101"
        # train_dir = "dataset/Test101"
        text_elements = get_all_text(train_dir)
        token_counters = get_text_counter(text_elements)

        term_doc_freq = get_doc_freq(token_counters)
        term_all_docs = sorted(term_doc_freq.keys())

        features = get_feature_training(term_doc_freq, term_all_docs, token_counters)

        training_result = open('training_result_feature.txt', 'w')
        training_result.writelines(json.dumps(features))
        training_result.close()
        training_result = open('training_result_token.txt', 'w')
        training_result.writelines(json.dumps(term_all_docs))
        training_result.close()
    training_result = open('training_result_feature.txt').read()
    training_features = json.loads(training_result)
    training_features = np.array(training_features)
    training_features = training_features.reshape((len(training_features), -1))

    training_result = open('training_result_token.txt').read()
    training_tokens = json.loads(training_result)

    # training_target = file_reader.get_target('dataset/topic/Training101.txt')
    training_target = file_reader.get_target('dataset/topic/Test101.txt')
    training_target = np.array(training_target)
    training_target = training_target.reshape((len(training_target), -1)).ravel()
    #
    # print training_features
    # print training_tokens
    # print training_target

    # # classifier
    # clf = svm.SVC(gamma=0.001, C=10000.)
    # clf = svm.SVC(gamma=0.001, C=10000.)
    # clf = svm.SVC()
    # clf = svm.LinearSVR()
    # clf = neighbors.KNeighborsClassifier(n_neighbors=5)
    clf = naive_bayes.BernoulliNB()
    # training_features = np.array(training_features)
    # # training_features = training_features.reshape((len(training_features), -1))
    # training_target = np.array(training_target)
    # # training_target = training_target.reshape((len(training_target), -1))
    # print len(training_features)
    # print 'here', len(training_target)
    clf.fit(training_features, training_target.ravel())
    # print 'TARGET', training_target
    # print 'RESULT', clf.predict(training_features)
    #
    # clf.fit(training_features[6:10], training_target[6:10])
    # print 'TARGET', training_target[6:10]
    # print 'RESULT', clf.predict(training_features[6:10])
    #
    # x = np.array([[0,0],[0,1],[1,0],[1,1]])
    # x = x.reshape(len(x), -1)
    # y = np.array([1,0,0,1])
    # y = y.reshape(len(y), -1)
    # print x, y
    # clf.fit(x, y.ravel())
    # print 'test', clf.predict(x)

    test_dir = "dataset/Test101"
    # test_dir = "dataset/Training101"
    text_elements = get_all_text(test_dir)
    token_counters = get_text_counter(text_elements)

    term_doc_freq = get_doc_freq(token_counters)
    term_all_docs = training_tokens

    features = get_feature_training(term_doc_freq, term_all_docs, token_counters)
    features = np.array(features)
    features = features.reshape((len(features), -1))
    # print len(features[0])
    # #
    # test_target = file_reader.get_target('dataset/topic/Training101.txt')
    test_target = file_reader.get_target('dataset/topic/Test101.txt')
    test_target = np.array(test_target)
    test_target = test_target.reshape((len(test_target), -1)).ravel()
    print test_target
    predicted = clf.predict(features)
    print predicted

    print("Classification report for classifier %s:\n%s\n" %
          (clf, metrics.classification_report(test_target, predicted)))
    print("Confusion matrix:\n%s" % metrics.confusion_matrix(test_target, predicted))
