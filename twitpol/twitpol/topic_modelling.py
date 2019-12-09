import gensim
from gensim import corpora
from gensim.utils import simple_preprocess
from tqdm import tqdm


def make_bow(docs):
    vocab = corpora.Dictionary(docs)
    corpus = [vocab.doc2bow(doc) for doc in docs]
    return corpus, vocab


def run_lda(corpus, vocab, num_topics=10):
    return gensim.models.ldamodel.LdaModel(
            corpus=corpus,
            id2word=vocab,
            num_topics=num_topics,
            update_every=1,
            passes=10,
            per_word_topics=True
        )
