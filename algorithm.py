"""
Project By:-

Nitesh Mishra(111915069)
Jimit Panditputra(111915082)
Alok Prakash(111915010)

Group-64

"""

from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
import re
import operator
import six

debug = False
test = False


def sentence_splitter(text):
    sentence_delimiters = re.compile(u'[\\[\\]\n.!?,;:\t\\-\\"()\\\'\u2019\u2013]')
    sentences = sentence_delimiters.split(text)
    return sentences


def stop_words_load(stop_word_file):
    stop_words = []
    for line in open(stop_word_file):
        if line.strip()[0:1] != "#":
            for word in line.split():
                stop_words.append(word)
    return stop_words


def word_separator(text, min_word_return_size):
    splitter = re.compile('[^a-zA-Z0-9_+\\-/]')
    words = []
    for single_word in splitter.split(text):
        current_word = single_word.strip().lower()
        if len(current_word) > min_word_return_size and current_word != '' and not is_number(current_word):
            words.append(current_word)
    return words


def build_stop_word_regex(stop_word_file_path):
    stop_word_list = stop_words_load(stop_word_file_path)
    stop_word_regex_list = []
    for word in stop_word_list:
        word_regex = '\\b' + word + '\\b'
        stop_word_regex_list.append(word_regex)
    stop_word_pattern = re.compile('|'.join(stop_word_regex_list), re.IGNORECASE)
    return stop_word_pattern


def is_number(s):
    try:
        float(s) if '.' in s else int(s)
        return True
    except ValueError:
        return False


def generate_candidate_keywords(sentence_list, stopword_pattern, min_char_length=1, max_words_length=5):
    phrase_list = []
    for s in sentence_list:
        tmp = re.sub(stopword_pattern, '|', s.strip())
        phrases = tmp.split("|")
        for phrase in phrases:
            phrase = phrase.strip().lower()
            if phrase != "" and is_acceptable(phrase, min_char_length, max_words_length):
                phrase_list.append(phrase)
    return phrase_list


def is_acceptable(phrase, min_char_length, max_words_length):
    if len(phrase) < min_char_length:
        return 0

    words = phrase.split()
    if len(words) > max_words_length:
        return 0

    digits = 0
    alpha = 0
    for i in range(0, len(phrase)):
        if phrase[i].isdigit():
            digits += 1
        elif phrase[i].isalpha():
            alpha += 1

    if alpha == 0:
        return 0

    if digits > alpha:
        return 0
    return 1


def word_score_calculator(phrase_List):
    word_frequency = {}
    word_degree = {}
    for phrase in phrase_List:
        word_list = word_separator(phrase, 0)
        word_list_length = len(word_list)
        word_list_degree = word_list_length - 1
        for word in word_list:
            word_frequency.setdefault(word, 0)
            word_frequency[word] += 1
            word_degree.setdefault(word, 0)
            word_degree[word] += word_list_degree
    for item in word_frequency:
        word_degree[item] = word_degree[item] + word_frequency[item]

    word_score = {}
    for item in word_frequency:
        word_score.setdefault(item, 0)
        word_score[item] = word_degree[item] / (word_frequency[item] * 1.0)

    return word_score


def generate_candidate_keyword_scores(phrase_list, word_score, min_keyword_frequency=1):
    keyword_candidates = {}

    for phrase in phrase_list:
        if min_keyword_frequency > 1:
            if phrase_list.count(phrase) < min_keyword_frequency:
                continue
        keyword_candidates.setdefault(phrase, 0)
        word_list = word_separator(phrase, 0)
        candidate_score = 0
        for word in word_list:
            candidate_score += word_score[word]
        keyword_candidates[phrase] = candidate_score
    return keyword_candidates


class Algorithm(object):
    def __init__(self, stop_words_path, min_char_length=1, max_words_length=5, min_keyword_frequency=1):
        self.__stop_words_path = stop_words_path
        self.__stop_words_pattern = build_stop_word_regex(stop_words_path)
        self.__min_char_length = min_char_length
        self.__max_words_length = max_words_length
        self.__min_keyword_frequency = min_keyword_frequency

    def run(self, text):
        sentence_list = sentence_splitter(text)

        phrase_list = generate_candidate_keywords(sentence_list, self.__stop_words_pattern, self.__min_char_length,
                                                  self.__max_words_length)

        word_scores = word_score_calculator(phrase_list)

        keyword_candidates = generate_candidate_keyword_scores(phrase_list, word_scores, self.__min_keyword_frequency)

        sorted_keywords = sorted(six.iteritems(keyword_candidates), key=operator.itemgetter(1), reverse=True)
        return sorted_keywords


if test:
    text = "File Error "

    sentenceList = sentence_splitter(text)
    stop_path = "document_similarity/Stoplist.txt"
    stop_word_pattern = build_stop_word_regex(stop_path)

    phrase_List = generate_candidate_keywords(sentenceList, stop_word_pattern)

    word_scores = word_score_calculator(phrase_List)

    keyword_candidates = generate_candidate_keyword_scores(phrase_List, word_scores)
    if debug: print(keyword_candidates)

    sortedKeywords = sorted(six.iteritems(keyword_candidates), key=operator.itemgetter(1), reverse=True)
    if debug: print(sortedKeywords)

    totalKeywords = len(sortedKeywords)
    if debug: print(totalKeywords)
    print(sortedKeywords[0:(totalKeywords // 3)])

    algo = Algorithm("Stoplist.txt")
    keywords = algo.run(text)
    print(keywords)
