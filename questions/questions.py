import math
import nltk
import os
import string
import sys

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()

    for file in os.listdir(directory):
        with open(os.path.join(directory, file)) as body:
            files[file] = body.read()

    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokens = nltk.word_tokenize(document.lower())
    # Filter out punctuation and stopwords
    words = [token for token in tokens if token not in string.punctuation and token not in nltk.corpus.stopwords.words("english")] 
    
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words_idf = dict()
    words = set()
    
    for document in documents:
        words = words.union({word for word in documents[document]})      

    for word in words:
        documents_containing = 0
        for document in documents.values():
            if word in document:
                documents_containing += 1

        words_idf[word] = math.log(len(documents)/documents_containing)

    return words_idf


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    ranking = dict()
        
    for filename, terms in files.items():
        score = 0
        
        for word in query:
            if word in terms:
                tf_idf = terms.count(word) * idfs[word]
                score += tf_idf       
        if score != 0:
            ranking[filename] = score
    
    return [filename for filename, score in sorted(ranking.items(), key=lambda x: x[1], reverse=True)][:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    ranking = dict()

    for sentence, terms in sentences.items():
        score = 0
        density = 0
        
        for word in query:
            if word in terms:
                score += idfs[word]
                density += terms.count(word) / len(terms)
        if score != 0:
            ranking[sentence] = (score, density) 

    return [sentence for sentence, measures in sorted(ranking.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)][:n]


if __name__ == "__main__":
    main()
