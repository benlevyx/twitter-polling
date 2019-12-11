import spacy
from tqdm import tqdm, tqdm_notebook

from twitpol import config


def get_nlp():
    stopwords = get_stopwords()
    nlp = spacy.load("en_core_web_lg")
    nlp.Defaults.stop_words.update(stopwords)
    for word in stopwords:
        lexeme = nlp.vocab[word]
        lexeme.is_stop = True

    def lemmstop(doc):
        return lemmatize_and_stop(nlp, doc)

    nlp.add_pipe(lemmstop, name='lemmatize_and_stop', after='ner')
    # nlp.add_pipe(remove_stopwords, name='stopwords', last=True)

    return nlp


def get_stopwords():
    stopwords = []
    with open(config.DATA / 'sentiment' / 'stopwords.txt') as f:
        lines = f.readlines()

    with open(config.DATA / 'topic_modelling' / 'stopwords.txt') as f:
        newlines = f.readlines()
    lines += newlines

    for i in range(1, len(lines)):
        stopwords.append(lines[i].strip())
    LEMMA_STOP = ['-PRON-', '\n', '\r', '\n\n', '\r\r']
    stopwords += LEMMA_STOP
    return list(set(stopwords))


def lemmatize_and_stop(nlp, doc):
    """Lemmatize a tweet
    """
    doc = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return doc
    # doc = u' '.join(doc)
    # return nlp.make_doc(doc)


def remove_stopwords(doc):
    doc = [token.text for token in doc if not token.is_stop and not token.is_punct]
    return doc


def make_docs(docs, nlp, notebook=False, extra_stop=None):
    if notebook:
        pbar = tqdm_notebook
    else:
        pbar = tqdm
    # res = []
    # for doc in pbar(nlp.pipe(docs)):
    #     res.append(doc)
    # return res
    return [nlp(doc) for doc in pbar(docs)]
    # res = []
    # for doc in pbar(docs):
    #     nlp_doc = nlp(doc)
    #     if extra_stop is not None:
    #         nlp_doc = [lemma for lemma in nlp_doc if lemma not in extra_stop]
    #     res.append(nlp_doc)
    # return res
