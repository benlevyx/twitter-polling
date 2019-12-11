"""Applying simple LDA topic modelling to detect what topics are most discussed
with respect to each candidate and pair of candidates
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
    corpus = pd.read_csv(config.DATA / 'processed' / 'lemmas.csv', index_col=0, engine='python')
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

        corpus[name] = corpus['tweet'].progress_apply(match)
    return corpus


def topic_model_candidates(corpus, nlp, queries, sample=-1):
    # models = {}
    topics = {}
    for c in config.CANDIDATES:
        print(f'Candidate {c}')
        cand_dict = {}
        extra_stop = [q.lower() for q in queries[c]]
        subset = corpus[corpus[c] == 1]
        for sent in ['pos', 'neg']:
            print(f'Sentiment: {sent}')
            if sent == 'pos':
                sent_subset = subset[subset['Sentiment'] > 0.8]
            else:
                sent_subset = subset[subset['Sentiment'] < 0.2]
            if sample > 0:
                sent_subset = sent_subset.sample(sample)
            model, lda_topics, log_perplexity = topic_model_corpus(sent_subset['lemmas'].tolist(), nlp, extra_stop=extra_stop)

            # models[c] = model
            sent_dict = {}
            sent_dict['topics'] = lda_topics
            sent_dict['log_perplexity'] = log_perplexity
            cand_dict[sent] = sent_dict
        topics[c] = cand_dict

        print(f'LDA results for {c}:')
        pprint(cand_dict)

    return topics


def remove_extra_stop(corpus, extra_stop):
    res = []
    for doc in tqdm(corpus):
        if type(doc) == float and np.isnan(doc):
            continue
        elif doc is None:
            continue
        else:
            nlp_doc = [lemma for lemma in doc if lemma not in extra_stop]
            res.append(nlp_doc)
    return res


def topic_model_corpus(corpus, nlp, extra_stop=None):
    print('Preprocessing...')
    if extra_stop is not None:
        corpus = remove_extra_stop(corpus, extra_stop)
    bow, vocab = topic_modelling.make_bow(corpus)
    print('Done.')
    print('Modelling...')
    model = topic_modelling.run_lda(bow, vocab, num_topics=10)  # Play with num_topics
    print('Done')
    lda_topics = model.print_topics()
    topic = lda_topics
    log_perplexity = model.log_perplexity(bow)

    return model, topic, log_perplexity


def save_topics(topics):
    with (config.DATA / 'topic_modelling' / 'topics.json').open('w') as fout:
        json.dump(topics, fout)


def main():
    nlp = language.get_nlp()
    queries = load_and_split_queries()
    corpus = load_corpus()

    # Sampling for testing
    # corpus = corpus.sample(50000)

    print('Doing topic modelling...')
    topics = topic_model_candidates(corpus, nlp, queries)
    save_topics(topics)
    print('Done.')


if __name__ == '__main__':
    main()
