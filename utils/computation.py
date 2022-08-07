import copy
import torch


def averageWeights(w):
    """
    Returns the average of the weights.
    """
    w_avg = copy.deepcopy(w[0])
    for key in w_avg.keys():
        for i in range(1, len(w)):
            w_avg[key] += w[i][key]
        w_avg[key] = torch.div(w_avg[key], len(w))
    return w_avg


def chunkList(lst: list, chunk_size: int):
    chunked_list = list()
    for i in range(0, len(lst), chunk_size):
        chunked_list.append(lst[i:i + chunk_size])
    return chunked_list
