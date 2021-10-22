"""
Project By:-

Nitesh Mishra(111915069)
Jimit Panditputra(111915082)
Alok Prakash(111915010)

Group-64

"""

import algorithm
import operator
from sklearn.feature_extraction.text import TfidfVectorizer
import pyttsx3
import webbrowser


class Main:
    def __init__(self, file):
        self.stop_word_removal()
        self.file = open(file, 'r', encoding="utf8")
        self.text = self.file.read()

    def stop_word_removal(self):
        self.stop_word = algorithm.Algorithm("Stoplist.txt", 4, 3, 3)

    def truncate_keyword(self, n):
        self.n = n
        self.keywords = self.keywords[0:self.n]
        return self.keywords

    def preprocess_transcript(self, transcript):
        self.stop_word_t = algorithm.Algorithm("Stoplist.txt", 4, 1, 3)
        self.transcript = open(transcript, 'r', encoding="utf8")
        self.t_text = self.transcript.read()

        self.t_keywords = self.stop_word_t.run(self.t_text)
        self.t_keywords = sorted(self.t_keywords, key=lambda l: l[1], reverse=True)
        return self.t_keywords

    def sort_keywords(self):
        self.keywords = self.stop_word.run(self.text)
        self.keywords = sorted(self.keywords, key=lambda l: l[1], reverse=True)
        return self.keywords

    def TfidfSimilarity(self, text1, text2):
        tfidf = vectorizer.fit_transform([text1, text2])
        x = (tfidf * tfidf.T).A[0, 1]

        return x

    def script_keys_to_list(self, keywords, n):
        script_list = []
        for i in range(n):
            script_list.append(keywords[i][0])
        return script_list


file = "script.txt"
vectorizer = TfidfVectorizer(stop_words='english')
k = Main(file)
keywords = k.sort_keywords()
n = 10
keywords = k.truncate_keyword(n)

engine = pyttsx3.init()
engine.setProperty("rate", 178)
script_list = k.script_keys_to_list(keywords, n)
print("List of extracted top n keywords are---", script_list)
transcript_files = ['transcript_1.txt', 'transcript_2.txt', 'transcript_3.txt']
key_score = []
final_score = []

for index in range(len(transcript_files)):

    t1_keywords = k.preprocess_transcript(transcript_files[index])
    trans1_list = k.script_keys_to_list(t1_keywords, len(t1_keywords))

    for i in range(n):
        tmp = 0

        for j in range(len(trans1_list)):
            tmp = tmp + k.TfidfSimilarity(script_list[i], trans1_list[j])
        key_score.append(tmp)

for i in range(n):
    final_score.append(key_score[i] + key_score[i + 10] + key_score[i + 20])

final_score = sorted(final_score, reverse=True)

print("PRINTING THE SORTED SCORE FOR EACH OF THE KEYWORDS -------->  ")
text = " "
total_key = " "
for i in range(n):
    if final_score[i] >= 1:
        text = text + script_list[i]
        print(script_list[i], "= \t", final_score[i])
    total_key = total_key + script_list[i]

engine.say("Top keywords extracted are ")
engine.say(total_key)
engine.runAndWait()

engine.say("Top 3 keywords are ")
engine.say(text)
engine.runAndWait()

search_terms = script_list[0]
engine.say("Opening google results for the top keyword")
engine.runAndWait()
url = "https://www.google.com.tr/search?q={}".format(search_terms)
webbrowser.open_new_tab(url)
