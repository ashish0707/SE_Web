import os
import re
from collections import defaultdict

import datetime

from DocumentParser import Parser


class NGramGenerator:

    def __init__(self):
        self.bi_gram_index = dict()
        self.tri_gram_index = dict()
        self.bi_gram_window = []
        self.tri_gram_window = []

    one_gram_corpus = dict()
    myParser = Parser()

    def generate_stopped_cleaned_files(self, folder, cleaned_file_path, stop_word_file_path):

        counter = 1
        if not os.path.exists(cleaned_file_path):
            print "Generating cleaned files... will take around 15 secs. please be patient."

            dict_of_stop_word = dict()
            for line in open(stop_word_file_path):
                dict_of_stop_word[line.replace("\n", "")] = 1

            os.mkdir(cleaned_file_path)
            for filename in os.listdir(folder):
                abs_fileName = os.path.join(folder, filename)
                raw_body_text = self.myParser.parse_document(abs_fileName)
                for line in raw_body_text.split("\n"):
                    cleaned_body_text = re.sub(r'[^\,\.\-\w\s]', '', line)  # apply regex on text extracted from html
                    cfilename = filename + ".txt"
                    abs_fileName = os.path.join(cleaned_file_path, cfilename)
                    with open(abs_fileName, 'a') as _file_:
                        for word in cleaned_body_text.split():
                            cleaned_word = self.clean_word(word)  # cleans the word using regex
                            if not cleaned_word in dict_of_stop_word:
                                _file_.write(cleaned_word.encode('utf8') + " ")  # write the cleaned word to the file
                    _file_.close()

                counter += 1
        else:
            print "cleaned files exist"

    def clean_word(self, word):
        if re.match(r'\d+.*,*\d+', word):
            word = word.rstrip(",")
            word = word.rstrip(".")
            return word.lower()
        else:
            return re.sub(r'[^\-\w\s]', '', word).lower()

    def generateIndex(self, folder):

        print "Generating corpus... will take around 15 secs. please be patient."
        begin = datetime.datetime.now()
        docId = 1
        for filename in os.listdir(folder):


            abs_fileName = os.path.join(folder, filename)
            for word in open(abs_fileName).read().split():
                self.add_to_one_gram_corpus(word, filename[:-4])  # adds unique words to the unigram corpus
                # self.add_to_bi_gram_corpus(word,filename[:-4])
                # self.add_to_tri_gram_corpus(word,filename[:-4])
            docId += 1

        print "Time to generate Unigram Corpus => " + str(datetime.datetime.now() - begin)


    # GIVEN   : a cleaned word and a documentId which is an integer
    # RETURNS : adds the word to one gram corpus.
    def add_to_one_gram_corpus(self, word, documenId):
        if word not in self.one_gram_corpus:
            self.one_gram_corpus[word] = Posting()
        self.one_gram_corpus[word].addToDocTermFreqDict(documenId)
        # print len(self.one_gram_corpus)


    # GIVEN   : a cleaned word and a documentId which is an integer
    # RETURNS : adds the word to bi gram index.

    def add_to_bi_gram_corpus(self, word, documenId):

        self.bi_gram_window.append(word)

        if len(self.bi_gram_window) == 2:
            temp = self.bi_gram_window[0] + self.bi_gram_window[1]
            if temp not in self.bi_gram_index:
                self.bi_gram_index[temp] = Posting()
            self.bi_gram_index[temp].addToDocTermFreqDict(documenId)
            self.bi_gram_window = []


    # GIVEN   : a cleaned word and a documentId which is an integer
    # RETURNS : adds the word to tri gram index.

    def add_to_tri_gram_corpus(self, word, documenId):

        self.tri_gram_window.append(word)

        if len(self.tri_gram_window) == 3:
            temp = self.tri_gram_window[0] + self.tri_gram_window[1] + self.tri_gram_window[2]
            if temp not in self.tri_gram_index:
                self.tri_gram_index[temp] = Posting()
            self.tri_gram_index[temp].addToDocTermFreqDict(documenId)
            self.tri_gram_window = []



    # print len(self.one_gram_corpus)

    def saveMapping(self, doc_id, filename):
        with open("mapping.txt", 'a') as _file_:
            tempData = "%d ==> " % doc_id + filename + "\n"
            _file_.write(tempData)
        _file_.close()

    def get_uni_gram_corpus(self):
        return self.one_gram_corpus


class Posting:
    def __init__(self):
        self.total = 0
        self.docTermFreqDict = defaultdict(int)


    def addToDocTermFreqDict(self,documentId):
        self.docTermFreqDict[documentId] += 1
        self.total += 1

    def __cmp__(self, posting):
        if self.total < posting.total:
            return -1
        if self.total == posting.total:
            return 0
        if self.total > posting.total:
            return 1

#
# ng = NGramGenerator()
# ng.generateUnigramCorpus()