import unicodedata
import re
import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from string import punctuation

def removeAccentedChars(posts):
    """Remove accented characters from scraped article.
    
    Arguments:
        list: The list of the articles scraped from the website
        
    Return:
        list: The cleaned list of articles 
    """

    replacement_patterns = [(r'(\w+)\'', '\g<1>'),(r'\[email protected\]', ''),(r'([{\',\?}])','')]
    text = []
    empty = ['']
    for post in posts:
        if post not in empty:
            patterns = [(re.compile(regex), repl) for (regex, repl) in replacement_patterns]
            
            for (pattern, repl) in patterns:
                (post, count) = re.subn(pattern, repl, post)
                pattern = re.compile(r'([{.}])')
                post = pattern.sub("\\1 ", post)
            text.append(unicodedata.normalize('NFKD', post.strip()).encode('ascii', 'ignore').decode('utf-8', 'ignore'))
            
    return text

def correctTextWords(post):
    """  Corrects article text from scraped website
    
    Arguments:
        text: The text data from an article to be lemmatized
        
    Return:
        text: The corrected text 
    """
    replacement_patterns = [
                           (r'won\'t', 'will not'),
                           (r'can\'t', 'cannot'),
                           (r'i\'m', 'i am'),
                           (r'ain\'t', 'is not'),
                           (r'(\w+)\'ll', '\g<1> will'),
                           (r'(\w+)n\'t', '\g<1> not'),
                           (r'(\w+)\'ve', '\g<1> have'),
                           (r'(\w+)\'s', '\g<1> is'),
                           (r'(\w+)\'re', '\g<1> are'),
                           (r'(\w+)\'d', '\g<1> would'),
                           (r'\[email protected\]', '')
                           ]
    
    patterns = [(re.compile(regex), repl) for (regex, repl) in replacement_patterns]
    post= post.replace('#MonitorUpdates http://bit.ly/2YF8FLJ', '')
    for (pattern, repl) in patterns:
        (post, count) = re.subn(pattern, repl, post)
        
    return post

def removeSpecialCharacters(post, remove_digits=False):
    """ Removes special characters from article text
    
    Arguments:
        text: The text data from an article from which sepecial 
        characters are to be removed
        
    Return:
        text: The text with removed special character
    """
    pattern = r"[^a-zA-z0-9$.,'\s]-" if not remove_digits else r"[^a-zA-z.,'\s]-"   
    post.encode('ascii',errors='replace').replace(b'?', b' ').decode('utf-8')
    post = re.sub(pattern, '', post)
        
    return post

def stemText(post):
    """ Takes text data and stem each word of the text
    
    Arguments:
        text: The text data from an article to be stem
        
    Return:
        text: The stemmed text 
    """
    lan_stem = LancasterStemmer()
    post = ' '.join([lan_stem.stem(word) for word in post.split()])
    
    return post

def lemmatizeText(post):
    """ Takes text data and lemmatizes each word of the text based on its POS tag if it is present
    
    Arguments:
        text: The text data from an article to be lemmatized
        
    Return:
        text: The lemmatized text 
    """
    word_net_lemma = WordNetLemmatizer()
    
    text = ' '.join([word_net_lemma.lemmatize(word) for word in post.split()])
    
    return text

def tokenizeText(post):
    """Tokenize a given text into list of sentenses and then list of words.
    
    Arguments:
        text: The text to be segmented into sentences and words.
    
    Return:
        A list of words from the text
    """
    special_char_pattern = re.compile(r'([{``.(-)!''}])')
    post = special_char_pattern.sub(" \\1 ", post)

    sentences = sent_tokenize(post)

    token_list = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        for word in words:
            token_list.append(word.lower())
        
    return token_list

def removeStopwords(post):
    """Remove stopwards from a given list of word token.
    
    Arguments:
        text: The word token from which stopwords are to be removed.
    
    Return:
        A list of words without stopwords
    """
    customstopward = set(stopwords.words('english')+list(punctuation))
    words=[word for word in post if word not in customstopward]
    pattern = re.compile('[{}]'.format(re.escape(punctuation)))
    empty = ['']
    filtered_tokens = [pattern.sub('', token) for token in words]
    filtered_tokens = [token for token in filtered_tokens if token not in empty]
        
    return filtered_tokens

def normalizedToken(text):
    """Normalizes a given text and return the list of normalized words.
    
    Arguments:
        text: the string or byte data input to be normalized and tokenized
        
    Return:
        A list of normalized tokens
    """
    posts = removeAccentedChars(text)

    normalized_tokens = []
    for post in posts:

        corrected_text = correctTextWords(post)
        removed_sp_char_text = removeSpecialCharacters(corrected_text)

        lemma_text = lemmatizeText(removed_sp_char_text)
        stemed_text = stemText(removed_sp_char_text)
#       tokenized_text = tokenizeText(lemma_text)
        tokenized_text = tokenizeText(stemed_text)
        removed_stopwords = removeStopwords(tokenized_text)
        normalized_tokens.append(removed_stopwords)
    
    return normalized_tokens

def normalizeText(text):
    """Normalizes a given text and return the list of normalized text.
    
    Arguments:
        text: the string or byte data input to be normalized
        
    Return:
        A list of normalized text
    """
    posts = removeAccentedChars(text)

    normalized_text = []
    for post in posts:

        corrected_text = correctTextWords(post)
        removed_sp_char_text = removeSpecialCharacters(corrected_text)
        normalized_text.append(removed_sp_char_text)
        
    return normalized_text

