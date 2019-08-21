from nltk.probability import FreqDist
from collections import defaultdict
from heapq import nlargest
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse.linalg import svds
import numpy as np
import networkx
from app.clean_text import normalizeText

def frequencyDistributionTextSummarizer(posts, num_sentences):
    """Summarises a given text and return the num_sentences.
    
    Arguments:
        text: the string or byte data to be summarised
        num_sentences: the number of sentences to be included in the summary
    
    Return:
        A string representing the summary
    """
    
    if num_sentences < 2:
        return 'Summary should be atleast 2 sentences long'
    
    summary_list = []
    
    for post in posts:

        sentences = sent_tokenize(post)
        if len(sentences) >= 2:
            important_words = normalizeText(post)
            frequency = FreqDist(important_words)

            ranking = defaultdict(int)

            for i, sentence in enumerate(sentences):
                for word in word_tokenize(sentence.lower()):
                    if word in frequency:
                        ranking[i] +=frequency[word]

            sentence_index = nlargest(num_sentences, ranking, key=ranking.get)

            summary = [sentences[i] for i in sorted(sentence_index)]
            summary_list.append(summary)
        else:
            return 'Text should have atleast 2 or more sentences.'

    return summary_list

def lsaTextSummarizer(docs, num_sentences, num_topics=1, sv_threshold=0.5):
    """Summarises a given text and return the n sentences.
    
    Arguments:
        text: the string or byte data to be summarised
        num_sentences: the number of sentences to be included in the summary
        sv_threshold: the sigma value threshold
        num_topics: the number of topics in the document
    
    Return:
        A list of paragraphs representing the summary
    """
    if num_sentences < 2:
        return 'Summary should be atleast 2 sentences long'
    
    summary_list = []

    for post in docs:

        sentences = sent_tokenize(post)
        if len(sentences) >= 2:
            vectorizer = TfidfVectorizer(min_df=1,ngram_range=(1, 1),stop_words='english')
            X_matrix = vectorizer.fit_transform(sentences)

            td_matrix = X_matrix.transpose()
            td_matrix = td_matrix.multiply(td_matrix > 0)

            u, s, vt = svds(td_matrix, k=num_topics)
            min_sigma_value = max(s) * sv_threshold

            s[s < min_sigma_value] = 0
            sent_scores = np.sqrt(np.dot(np.square(s), np.square(vt)))

            top_sentence_indices = sent_scores.argsort()[-num_sentences:][::-1]
            top_sentence_indices.sort()
            summary = []
            for index in top_sentence_indices:
                summary.append(sentences[index])
            summary_list.append(summary)
        else:
            return 'Text should have atleast 2 or more sentences.'

    return summary_list

def textRankTextSummarizer(docs, num_sentences):
    """Summarizes a given document and return the n sentences.
    
    Arguments:
        text: the string or byte document to be summarised
        num_sentences: the number of sentences to be included in the summary
    
    Return:
        A list of paragraphs representing the summary
    """
    if num_sentences < 2:
        return 'Summary should be atleast 2 sentences long'
    
    summary_lists = []
    for post in docs:

        sentences = sent_tokenize(post)
        if len(sentences) >= 2:
            vectorizer = TfidfVectorizer(min_df=1,ngram_range=(1, 1),stop_words='english')
            X_matrix = vectorizer.fit_transform(sentences)

            similarity_matrix = (X_matrix * X_matrix.T)
            similarity_graph = networkx.from_scipy_sparse_matrix(similarity_matrix)

            scores = networkx.pagerank(similarity_graph)
            ranked_sentences = sorted(((score, index) for index, score in scores.items()), reverse=True)

            top_sentence_indices = [ranked_sentences[index][1] for index in range(num_sentences)]
            top_sentence_indices.sort()

            summary = []
            for index in top_sentence_indices:
                summary.append(sentences[index])
            summary_lists.append(summary)
        else:
            return 'Text should have atleast 2 or more sentences.'

    return summary_lists
