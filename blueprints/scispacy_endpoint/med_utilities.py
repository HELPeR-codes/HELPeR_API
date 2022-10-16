from sentence_transformers import util


def scoring(pair, EN):
    # vecs =
    query_vec_1 = EN.encode(pair[0])
    query_vec_2 = EN.encode(pair[1])
    sim = round(util.pytorch_cos_sim(query_vec_1, query_vec_2).item(), 5)
    return sim

