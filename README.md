# document_similarity
-The Aim of this project is to create a model to check similarity between documents and show google results for the top keyword. It focuses on recognizing keywords from the 
document and comparing them using final score with the help of cosine similarity.
-There are two types of files the script and the transcript file(can be multiple) as a form of input of documents whose similarity needs to be checked. To run the project, run the main.py file(ensure all the libraries are pre-installed) after replacing the script.txt and transcript.txt with the document files in .txt format. 
-Upon running, the output will be in the form of top 10 keywords(phares) in the documents (both in written format and spoken by the machine )with the similarity scores of top 3 
of them. 
	-If the documenst are similar, the code will automatically redirect to google with input as the top keyword.
	-If the documents are not similar( by running the main2.py file) the error message is printed saying "Documents not similar"
-The main.py file contains the main working of the project using cosine similarity and the algorythm.py file contains the code to perform keyword extraction after stopword removal from the documents. The main2.py file is same as the main.py file, but just different input documnets to show documents do not match.
-Keywords, defined as a sequence of one or more words, provide a compact representation of a document’s content. Ideally, keywords represent in condensed form the essential 
content of a document.
-Score of the Keywords
  -Degree = number of words in the keyword phrase -1
  -Frequency = number of times the keyword appeared in the document
  -Final Score = (degree/frequency)
  -Thus, Total score of a keyword phrase = sum of each of its keyword scores
-Created by:
	Jimit Panditputra	
	Nitesh Mishra	
	Alok Prakash
