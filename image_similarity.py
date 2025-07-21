from sklearn.metrics.pairwise import cosine_similarity

def find_similar(feature, db_features):
    sims = cosine_similarity(feature, db_features)
    idx = sims.argmax()
    return idx, sims[0][idx]
