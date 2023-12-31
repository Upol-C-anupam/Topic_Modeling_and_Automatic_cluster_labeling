import numpy as np
import pandas as pd
import random as rn
import re
import nltk
import os

import matplotlib.pyplot as plt
import seaborn as sns
from plotly import graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff

from nltk.corpus import stopwords
from wordcloud import WordCloud

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

pd.set_option("display.max_rows", 600)
pd.set_option("display.max_columns", 500)
pd.set_option("max_colwidth", 400)



import umap  # dimensionality reduction
import hdbscan  # clustering
from functools import partial

# To perform the Bayesian Optimization for searching the optimum hyperparameters,
# I use hyperopt package:
from hyperopt import fmin, tpe, hp, STATUS_OK, space_eval, Trials
import random


def generate_clusters(
    message_embeddings,
    n_neighbors,
    n_components,
    min_cluster_size,
    min_samples=None,
    random_state=None,
):
    
    umap_embeddings = (
        umap.UMAP(
            n_neighbors=n_neighbors,
            n_components=n_components,
            metric="cosine",
            random_state=random_state,
        )
    ).fit_transform(message_embeddings)

    clusters = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        metric="euclidean",
        gen_min_span_tree=True,
        cluster_selection_method="eom",
    ).fit(umap_embeddings)

    return clusters


## Hyperopt


def score_clusters(clusters, prob_thresh0ld=0.05):
 
    cluster_labels = clusters.labels_

    label_count = len(np.unique(cluster_labels))
    total_num = len(clusters.labels_)

    cost = np.count_nonzero(clusters.probabilities_ < prob_thresh0ld) / total_num

    return label_count, cost


def objective(params, embeddings, label_lower, label_upper):

    clusters = generate_clusters(
        embeddings,
        n_neighbors=params["n_neighbors"],
        n_components=params["n_components"],
        min_cluster_size=params["min_cluster_size"],
        random_state=params["random_state"],
    )

    label_count, cost = score_clusters(clusters, prob_thresh0ld=0.05)

    if (label_count < label_lower) | (label_count > label_upper):
        penalty = 1.0
    else:
        penalty = 0

    loss = cost + penalty

    return {"loss": loss, "label_count": label_count, "status": STATUS_OK}


# Then minimize the objective function over the hyperparameter search space using the
# Tree-structured Parzen Estimator (TPE) algorithm:
def bayesian_search(embeddings, space, label_lower, label_upper, max_evals=100):
   

    trials = Trials()
    fmin_objective = partial(
        objective,
        embeddings=embeddings,
        label_lower=label_lower,
        label_upper=label_upper,
    )

    best = fmin(
        fmin_objective,
        space=space,
        algo=tpe.suggest,
        max_evals=max_evals,
        trials=trials,
    )

    best_params = space_eval(space, best)
    print("best:")
    print(best_params)
    print(f"label count: {trials.best_trial['result']['label_count']}")

    best_clusters = generate_clusters(
        embeddings,
        n_neighbors=best_params["n_neighbors"],
        n_components=best_params["n_components"],
        min_cluster_size=best_params["min_cluster_size"],
        random_state=best_params["random_state"],
    )

    return best_params, best_clusters, trials