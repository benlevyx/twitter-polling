"""Applying simple LDA topic modelling to detect what topics are most discussed
with respect to each candidate and pair of candidates
"""
import json

import pandas as pd
import numpy as np
import spacy
import gensim
from tqdm import tqdm

from twitpol import config, topic_modelling, language, utils


tqdm.pandas()


def load_corpus():
    csv_files = (config.DATA / 'big_data').glob('*.csv')
    corpus = pd.concat([pd.read_csv(f, index_col=0) for f in csv_files], axis=0, sort=False)
    cols = [c for c in corpus.columns if 'Unnamed' not in c]
    corpus = corpus[cols]
    print(corpus.shape)
    return corpus


def match_to_candidates(corpus):
    queries = utils.get_queries()
    split_queries = {}
    for name, query in queries:
        split_queries[name] = [q.strip('"') for q in query.split(' OR ')]

    for name, terms in split_queries.items():
        print(f'Checking if tweets match {name}')

        def match(tweet):
            for q in terms:
                if q in tweet:
                    return True
            return False

        corpus[name] = corpus['tweet'].progress_apply(match)
    return corpus


def topic_model_candidates(corpus, nlp):
    models = {}
    topics = {}
    for c in config.CANDIDATES:
        print(f'Preprocessing tweets for {c}')
        subset = corpus[corpus[c]]
        docs = language.make_docs(subset['tweet'].tolist(), nlp)
        bow, vocab = topic_modelling.make_bow(docs)
        lda_model = topic_modelling.run_lda(bow, vocab, num_topics=10)  # Play with num_topics
        models[c] = lda_model
        lda_topics = lda_model.print_topics()
        topics[c] = lda_topics

        print(f'Topics for {c}:')
        print(lda_topics)

    return models, topics


def save_topics(topics):
    with (config.DATA / 'topic_modelling' / 'topics.json').open('w') as fout:
        json.dump(topics, fout)


def main():
    nlp = language.get_nlp()
    corpus = load_corpus()
    corpus = match_to_candidates(corpus)
    models, topics = topic_model_candidates(corpus, nlp)
    save_topics(topics)


if __name__ == '__main__':
    main()
