from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
import numpy as np
import pickle

def kMeansCluster(posts):
    """Classifies a given document and return the classified document.

    Arguments:
        text: the string or byte document to be classified

    Return:
        A dictionary of classified document
    """
    articles = []
    text = {}
    for post in posts:
        articles += post

    vectorizer = TfidfVectorizer(max_df=0.5,min_df=2,stop_words='english')
    X = vectorizer.fit_transform(articles)

    km = KMeans(n_clusters=5,init='k-means++',max_iter=100, n_init=1,verbose=True)
    km.fit(X)

    np.unique(km.labels_, return_counts=True)

    for i, cluster in enumerate(km.labels_):
        oneArticle = articles[i]
        if cluster not in text.keys():
            text[cluster] = oneArticle
        else:
            text[cluster] += oneArticle
    return vectorizer, X, km, text

def affinityPropagationCluster(posts):
    """Classifies a given document and return the classified document.

    Arguments:
        text: the string or byte document to be classified

    Return:
        A dictionary of classified document
    """
    articles = []
    text = {}
    for post in posts:
        articles += post
        
    vectorizer = TfidfVectorizer(max_df=0.5,min_df=2,stop_words='english')
    ap_X = vectorizer.fit_transform(articles)
    
    sim = ap_X * ap_X.T
    sim = sim.todense()
    
    ap = AffinityPropagation()
    ap.fit(sim)
    
    np.unique(ap.labels_, return_counts=True)

    for i, cluster in enumerate(ap.labels_):
        oneArticle = articles[i]
        if cluster not in text.keys():
            text[cluster] = oneArticle
        else:
            text[cluster] += oneArticle
    return text

def agglomerativeCluster(posts):
    """Classifies a given document and return the classified document.

    Arguments:
        text: the string or byte document to be classified

    Return:
        A dictionary of classified document
    """
    articles = []
    text = {}
    for post in posts:
        articles += post
        
    vectorizer = TfidfVectorizer(max_df=0.5,min_df=2,stop_words='english')
    ac_X = vectorizer.fit_transform(articles)
    
    sim = ac_X * ac_X.T
    sim = sim.todense()
    
    ac = AgglomerativeClustering(n_clusters=4)
    ac.fit(sim)
    
    np.unique(ac.labels_, return_counts=True)

    for i, cluster in enumerate(ac.labels_):
        oneArticle = articles[i]
        if cluster not in text.keys():
            text[cluster] = oneArticle
        else:
            text[cluster] += oneArticle
    return text

def loadModel():
    """Loads the classification model for clustering new articles
    """
    km_model = pickle.load(open('./app/databases/model/km_model.sav', 'rb'))

    return km_model

def classifyArticles(posts):
    """Classifies a given document and return the class.

    Arguments:
        text: the string or byte document to be classified

    Return:
        A list with document index and thier clusters
    """
    article = ''
    sents = []
    cluster = []

    for post in posts:
        sents += [sent for sent in post]
        article = ' '.join(sent for sent in sents)
        vector = pickle.load(open('./app/databases/model/km_vector.sav', 'rb'))
        data = vector.transform([article])
        model = pickle.load(open('./app/databases/model/km_model.sav', 'rb'))
        cluster.append(model.predict(data)[0])
    return cluster
