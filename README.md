

I have done Topic modeling with BERT based sentence transformer model.

[Dataset Link](https://zenodo.org/record/1000885#.YxxQ7NJBxhF)


For labeling the topic  I have used a technique named Automatic  Cluster Labeling which was first  proposed in 2021 in this paper [Research Paper -Open Intent Discovery through Unsupervised Semantic Clustering and Dependency Parsing ](https://arxiv.org/pdf/2104.12114.pdf)
I hace concatinated most common verbs, direct objects top two noun for each text cluster for labeling the topic.

I used all_mpnet_basev2 as sentence transformer leveraging it's quality to map sentence and paragraphs into 768 dimesnional vector space.
For dimensionality reduction I have used uniform manifold approximation and projection (UMAP),  as it is much faster and more scalable then other techniques it preserves global structures of data much better. 
It is useful for both visualization and as a preprocessing dimensionality reduction step before clustering. 
Hyperopt is used for handeling bayesian optimization for searching optimal parameters.

[Sentence Embedding](https://towardsdatascience.com/clustering-sentence-embeddings-to-identify-intents-in-short-text-48d22d3bf02e)
