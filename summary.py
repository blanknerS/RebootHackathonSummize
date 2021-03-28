#Blake Ankner
import urllib.request
import bs4 as bs
import nltk
import re
import heapq

def summarize(text):
    source_text = text
    source_text = re.sub(r'\[[0-9]*\]', ' ', source_text)
    source_text = re.sub(r'\s+', ' ', source_text)

    formatted_source_text = re.sub('[^a-zA-Z]', ' ', source_text )
    formatted_source_text = re.sub(r'\s+', ' ', formatted_source_text)

    sentence_list = nltk.sent_tokenize(source_text)
    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_source_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    summary_sentences = heapq.nlargest(3, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)
    return summary
