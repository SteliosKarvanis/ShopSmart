"""Calls clusterize.eval_clusterization woth different hyperparametrizations

Call me from inside tools/
"""

from clusterize import eval_clusterization

from thefuzz import fuzz as tfuzz  # string similarities
from rapidfuzz import process, fuzz
import numpy as np

def geomean(tags1, tags2):
    """geometric mean of set ratios"""
    combined_score = 1
    n_scores = 0
    for label in ["PRO", "MAR", "ESP", "TAM", "QUA"]:
        if label not in tags1 and label not in tags2:
            continue # ignore labels absent from both tag sets (uninformative)
        if label not in tags1 or label not in tags2:
            combined_score = 0 # TODO too consrevative? We are zeroing out the whole score if a tag appears in only one of the args
            n_scores += 1
        else:
            label_score = tfuzz.token_set_ratio(tags1[label], tags2[label])
            # label_score /= 100  # fuzz returns value in 0-100 range
            combined_score *= label_score
            n_scores += 1
    return np.array(combined_score ** (1 / n_scores), dtype=np.int8)

eval_clusterization(geomean, 80)
