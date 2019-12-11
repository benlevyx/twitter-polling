"""Preprocessing

1. Combining tweets into single dataframe
2. Matching to candidates
3. Removing stopwords and converting to lemmas
"""
import json
import itertools as it
from pprint import pprint

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
    return corpus


def load_and_split_queries():
    queries = utils.get_queries()
    split_queries = {}
    for name, query in queries:
        split_queries[name] = [q.strip('"') for q in query.split(' OR ')]
    return split_queries


def match_to_candidates(corpus, queries):
    for name, terms in queries.items():
        print(f'Checking if tweets match {name}')

        def match(tweet):
            for q in terms:
                if q in tweet:
                    return True
            return False

        corpus[name] = corpus['tweet'].progress_apply(match).astype(int)
    return corpus


def main():
    nlp = language.get_nlp()
    queries = load_and_split_queries()

    print('Loading corpus...')
    corpus = load_corpus()
    print('Done.')

    # For scalability
    corpus = corpus.sample(1000000)

    print('Matching to candidates...')
    corpus = match_to_candidates(corpus, queries)
    print('Done')

    print('Removing stopwords and lemmatizing...')
    corpus['lemmas'] = language.make_docs(corpus['tweet'].tolist(), nlp)
    corpus.drop('tweet', axis=1)
    print('Done')

    # Saving
    print('Saving...')
    corpus.to_csv(config.DATA / 'processed' / 'lemmas.csv')
    print('Done')


if __name__ == '__main__':
    main()
