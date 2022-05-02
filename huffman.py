import numpy as np
import matplotlib.pyplot as plt
import cv2
import math


class Node:
    def __init__(self, character, probability, right=None, left=None):
        self.character = character
        self.probability = probability
        self.right = right
        self.left = left


def insertInto(node, list):
    for i in range(len(list)):
        if list[i].probability <= node.probability:
            list.insert(i, node)
            return
    list.append(node)


def createTree(prob):
    nodes = []
    val = list(prob.values())
    keys = list(prob.keys())
    for i in range(len(val)):
        nodes.append(Node([keys[i]], val[i]))
    nodes.sort(key=lambda x: x.probability, reverse=True)
    while len(nodes) > 1:
        right = nodes.pop()
        left = nodes.pop()
        newnode = Node((right.character + left.character), (right.probability + left.probability), right, left)
        insertInto(newnode, nodes)
    return nodes[0]


def getValue(character, root, newsymbol):
    if (root.left and root.right) is None:
        return newsymbol
    else:
        if character in root.left.character:
            newsymbol = getValue(character, root.left, newsymbol+"0")
        else:
            newsymbol = getValue(character, root.right, newsymbol+"1")
        return newsymbol


def countElements(inputdata):
    hist_data = {}
    for i in inputdata:
        for j in i:
            if hist_data.__contains__(j):
                hist_data[j] += 1
            else:
                hist_data[j] = 1
    return hist_data


def probability(hist_data):
    prob = [x / sum(list(hist_data.values())) for x in list(hist_data.values())]
    keys = list(hist_data.keys())
    return dict(zip(keys, prob))


def histogram(prob, depth=255):
    val = list(prob.values())
    keys = list(prob.keys())
    plt.figure(figsize=(10, 5))
    plt.xlim(0, depth)
    plt.bar(keys, val, color='#969696')


def entropy(prob):
    entr = 0
    val = list(prob.values())
    for i in val:
        entr += i * (-math.log(i, 2))
    return entr


def readPgm(filename):
    inputdata = cv2.imread(filename)
    raster = []
    for y in inputdata:
        row = []
        for x in y:
            row.append(x[0])
        raster.append(row)
    return raster


def averageLength(data):
    avg = 0
    dict = probability(countElements(data))
    for i in list(dict.items()):
        avg += i[1] * len(i[0])
    return avg


def coder(inputdata, model=None):
    if model == 'model1':
        hist_data = countElements(inputdata)
        prob = probability(hist_data)
        histogram(hist_data)
        plt.show()
        print('The entropy: ', entropy(prob))
        root = createTree(prob)
        for i in range(len(inputdata)):
            for j in range(len(inputdata[i])):
                inputdata[i][j] = getValue(inputdata[i][j], root, "")
        return inputdata
    elif model == 'model2':
        #TODO
        print('not implemented yet')
    elif model == 'model3':
        #TODO
        print('not implemented yet')
    else:
        print('not implemented yet')


def decoder():
    return 0


inputdata = readPgm('rozklady/geometr_05.pgm')
outputdata = coder(inputdata, 'model1')
print('The average codeword length: ', averageLength(outputdata))