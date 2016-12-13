from collections import defaultdict

import collections

import time

from Corpus import NGramGenerator
from cosine_similarity import CosineSimilarity

myGenerator = NGramGenerator()

myGenerator.generate_stopped_cleaned_files("/Users/ashishbulchandani/PycharmProjects/SE_Web/wiki_webpages",
                                        "/Users/ashishbulchandani/PycharmProjects/SE_Web/cleaned_files",
                                        "/Users/ashishbulchandani/PycharmProjects/SE_Web/common_words.txt")

myGenerator.generateUnigramCorpus("/Users/ashishbulchandani/PycharmProjects/SE_Web/cleaned_files")



# for k,v in myGenerator.one_gram_corpus.items():
#     print k
#     for ik, iv in v.docTermFreqDict.items():
#         print " %d => %d"%(ik,iv)

cs = CosineSimilarity()

cs.createMatix(myGenerator.one_gram_corpus)
# Input, parse the query and generate weight for each term
query_word_and_tf = defaultdict(int)
query_number = 1
var = ""


def getFormatedDockey(docKey):
    space = " "
    for i in range(60 - len(docKey)):
     space += " "
    docKey += space
    return docKey



while True:

    # ask user to input query
    var = raw_input("Please enter query or 'q' to quit: ")
    begin = time.time()
    if var.lower() == "q":
        break

    for word in var.split():
        query_word_and_tf[word] += 1

        # get each document score for the given query
    doc_and_score_dict = cs.calculateSimilarity(query_word_and_tf, len(query_word_and_tf))

        # sort the documents in descending order of their score
    sortedDocIds = sorted(doc_and_score_dict.items(), key=lambda t: t[1], reverse=True)

        # counter = 1
        # for value in sortedDocIds:
        #     print value
        #     if counter > 5:
        #         break
    counter = 0
    resultArray = []
    for value in sortedDocIds:
        resultArray.append("https://en.wikipedia.org/wiki/" + '_'.join(value[0][:-16].split()))
        print resultArray[counter]
        if counter > 10:
            break
        counter+=1

        # save the top 100 files as best match for given query
        # rank = 1
        # query_file_name = "q"+str(query_number)+"-top-100-results.txt"
        #
        # with open(query_file_name, 'a') as _file_:
        #     for docKey, score in collections.OrderedDict(sortedDocIds).items():
        #         formatedText = "%d  Q0  " % query_number
        #
        #         formatedText += getFormatedDockey(docKey) + "  %d   %f vector_space_without_normalization" % (rank, score)
        #         _file_.write(formatedText+"\n")
        #         rank += 1
        #         if rank > 100:
        #             break
        #         # print (formatedText)
        #
        # _file_.close()
        # query_number += 1
    print "Query Processed in ==> " + str(time.time() - begin)

#*********************** QUERIES **************************

# global warming potential
# green power renewable energy
# solar energy california
# light bulb bulbs alternative alternatives
