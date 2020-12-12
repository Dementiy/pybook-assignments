import gensim
import pyLDAvis.gensim
from gensim.corpora import Dictionary
from textacy import preprocessing
from tqdm import tqdm

from vkapi.wall import get_wall_execute


def example():
    posts = get_wall_execute(domain="rbc", count=5000, max_count=1000, progress=tqdm)
    stopwords = list(map(str.strip, open("stop_words.txt")))
    text_no_urls = map(preprocessing.replace.replace_urls, posts.text.dropna().to_list())
    text_no_punct = map(preprocessing.remove_punctuation, text_no_urls)
    text_no_emojis = map(preprocessing.replace.replace_emojis, text_no_punct)
    text_no_white_space = map(preprocessing.normalize.normalize_whitespace, text_no_emojis)
    docs = map(str.split, text_no_white_space)
    docs = [[word.lower() for word in doc if word not in stopwords] for doc in docs]
    docs = [[word for word in doc if word not in stopwords] for doc in docs]
    dictionary = Dictionary(docs)
    corpus = list(dictionary.doc2bow(text) for text in docs)
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=10, id2word=dictionary, passes=15)
    vis = pyLDAvis.gensim.prepare(ldamodel, corpus, dictionary)
    pyLDAvis.show(vis)


if __name__ == "__main__":
    example()
