import json
from collections import defaultdict

from flask import Flask,render_template, request
import time
from Corpus import NGramGenerator
from cosine_similarity import CosineSimilarity

app = Flask(__name__)



myGenerator = NGramGenerator()
myGenerator.generateUnigramCorpus("cleaned_files")



# for k,v in myGenerator.one_gram_corpus.items():
#     print k
#     for ik, iv in v.docTermFreqDict.items():
#         print " %d => %d"%(ik,iv)

cs = CosineSimilarity()

cs.createMatix(myGenerator.one_gram_corpus)


@app.route("/")
def main():
    return render_template('/index.html')

@app.route('/search' ,methods=['POST'])
def search():
    resultArray = []
    now = time.time()
    query_word_and_tf = defaultdict(int)
    # read the posted values from the UI
    _query= request.form['query']
    print _query


    for word in _query.lower().split():
        query_word_and_tf[word] += 1

    # get each document score for the given query
    doc_and_score_dict = cs.calculateSimilarity(query_word_and_tf, len(query_word_and_tf))

    # sort the documents in descending order of their score
    sortedDocIds = sorted(doc_and_score_dict.items(), key=lambda t: t[1], reverse=True)

    counter = 1
    for value in sortedDocIds:
        resultArray.append("https://en.wikipedia.org/wiki/"+ '_'.join(value[0][:-16].split()))
        print resultArray[counter-1]
        if counter > 10:
            break
        counter +=1

    return json.dumps({'totaltime':str(time.time() - now) + " seconds", 'urls': resultArray})

    # return "new query"

if __name__ == "__main__":
    app.run()