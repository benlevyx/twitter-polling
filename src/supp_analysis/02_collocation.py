import numpy as np
import pandas as pd
from tqdm import tqdm

from twitpol import config


def load_corpus():
    corpus = pd.read_csv(config.DATA / 'processed' / 'lemmas.csv', index_col=0)
    print(corpus.shape)
    return corpus


def collocation_matrix(corpus):
    n_cands = len(config.CANDIDATES)
    coll_mat = np.zeros((n_cands, n_cands))
    pbar = tqdm(total=n_cands**2)
    for i, c1 in enumerate(config.CANDIDATES):
        for j, c2 in enumerate(config.CANDIDATES):
            coll_mat[i, j] = np.sum(np.logical_and(corpus[c1], corpus[c2]))
            pbar.update()
    pbar.close()
    return coll_mat


def save_coll_mat(coll_mat, fout):
    df = pd.DataFrame(coll_mat,
                      index=config.CANDIDATES,
                      columns=config.CANDIDATES)
    df.to_csv(fout)


def main():
    print("Loading corpus")
    corpus = load_corpus()
    print("Done.")

    print('Making collocation matrix...')
    coll_mat = collocation_matrix(corpus)
    save_coll_mat(coll_mat, config.DATA / 'collocation' / 'collocation_matrix.csv')
    print('Done.')
