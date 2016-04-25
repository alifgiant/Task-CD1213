__author__ = 'maakbar'

from sklearn import svm, metrics

if __name__ == "__main__":
    feature = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]
    target = [0, 0, 0, 0, 0, 0, 0, 1]
    clf = svm.SVC(gamma=0.01, C=1000.)
    clf.fit(feature, target)

    print clf.predict(feature)


