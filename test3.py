#!/usr/bin/env python
# coding=utf-8
import jieba

import time
import re
import os
import sys
import codecs
import shutil
import numpy as np
import matplotlib
import scipy
import matplotlib.pyplot as plt
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer


def read_from_file(file_name):
    with open(file_name, "r") as fp:
        words = fp.read()
    return words


def stop_words(stop_word_file):
    words = read_from_file(stop_word_file)
    result = jieba.cut(words)
    new_words = []
    for r in result:
        new_words.append(r)
    return set(new_words)


def del_stop_words(words, stop_words_set):
    #   words是已经切词但是没有去除停用词的文档。
    #   返回的会是去除停用词后的文档
    result = jieba.cut(words)
    new_words = []
    for r in result:
        if r not in stop_words_set:
            new_words.append(r)
    return new_words

def listContent():
    returnList = []
    stop_content = stop_words("./doc/stop_word.txt")

    for i in range(1,1500):
        fileName = "./doc/"+str(i)+".txt";
        print fileName
        file_content = read_from_file(fileName)
        del_stop_word_content = del_stop_words(file_content, stop_content)
        raw_content = ""
        for out in del_stop_word_content:
            raw_content = raw_content + out.encode("utf-8") + " "
        print raw_content
        returnList.append(raw_content)

    return returnList
answer = listContent()


#########################################################################
#                           第一步 计算TFIDF



# 参考: http://blog.csdn.net/abcjennifer/article/details/23615947
# vectorizer = HashingVectorizer(n_features = 4000)

# 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
vectorizer = CountVectorizer()

# 该类会统计每个词语的tf-idf权值
transformer = TfidfTransformer()

# 第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
tfidf = transformer.fit_transform(vectorizer.fit_transform(answer))

# 获取词袋模型中的所有词语
word = vectorizer.get_feature_names()

# 将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
weight = tfidf.toarray()

# 打印特征向量文本内容
print 'Features length: ' + str(len(word))
resName = "BHTfidf_Result.txt"
result = codecs.open(resName, 'w', 'utf-8')
for j in range(len(word)):
    result.write(word[j] + ' ')
result.write('\r\n\r\n')

# 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
for i in range(len(weight)):
    # print u"-------这里输出第", i, u"类文本的词语tf-idf权重------"
    for j in range(len(word)):
        # print weight[i][j],
        result.write(str(weight[i][j]) + ' ')
    result.write('\r\n\r\n')

result.close()

########################################################################
#                               第二步 聚类Kmeans

print 'Start Kmeans:'
from sklearn.cluster import KMeans

clf = KMeans(n_clusters=14)  # 定为几类
print "weight= "+str(weight)       #weight 为[][] 是所有的tf-idf的值
s = clf.fit(weight)
print s

'''
print 'Start MiniBatchKmeans:'
from sklearn.cluster import MiniBatchKMeans
clf = MiniBatchKMeans(n_clusters=20)
s = clf.fit(weight)
print s
'''

# 中心点
print(clf.cluster_centers_)

# 每个样本所属的簇
label = []  # 存储1000个类标 4个类
print(clf.labels_)
i = 1
while i <= len(clf.labels_):
    print i, clf.labels_[i - 1]
    label.append(clf.labels_[i - 1])
    i = i + 1

# 用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数  958.137281791
print(clf.inertia_)



