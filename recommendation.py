# coding=utf-8
"""
Personality Recommendation
"""
import cPickle
import math
import random
class UserItemRecommendation():
    """
    based on user recommendation.
    we chose the top k items from the n nearest user of u, witch have never concerned by u.
    """
    def __init__(self):
        self.W = None  # W[u][v] is the similarity between u and v

    def save(self, file="user_item_model"):
        cPickle.dump(self.W, open(file,"wb"))

    def load(self, file="user_item_model"):
        self.W = cPickle.load(open(file, "rb"))

    def userSimilarity(self, train):
        """
        calculate pairs users' similarity
        :param train: dict(user_id:dict(item_id, scores))
        :return:
        """
        item_users = dict()
        for u, items in train.items():
            for i in items.keys():
                if i not in item_users:
                    item_users[i] = set()
                item_users[i].add(u)
        # calculate co-rated items between users
        C = dict()
        N = dict()
        for i, users in item_users.items():
            for u in users:
                if u not in N:
                    N[u] = 0
                N[u] += 1
                if u not in C:
                    C[u] = dict()
                for v in users:
                    if u == v:
                        continue
                    if v not in C[u]:
                        C[u][v] = 0
                    C[u][v] += 1 / math.log(1 + len(users))
        # calculate finial similarity matrix W
        W = dict()
        for u, related_users in C.items():
            if u not in W:
                W[u] = dict()
            for v, cuv in related_users.items():
                W[u][v] = cuv / math.sqrt(N[u] * N[v])
        self.W = W

    def recommendate(self, user, train, k):
        """
        get recommendation from the k nearest user
        :param train:
        :param W:
        :param k:
        :return:
        """
        rank = dict()
        interacted_items = train[user]
        k_users_smi = sorted(self.W[user].items(), key=lambda x: x[1], reverse=True)[0:k]
        for v, wuv in k_users_smi:
            for i, rvi in train[v].items():
                if i in interacted_items:
                    continue
                if i not in rank:
                    rank[i] = 0
                rank[i] += wuv * rvi
        return rank

    def getRecommendation(self, user, train, N, k):
        """
        get N items from recommendation system
        :param user:
        :param train:
        :param N:
        :param k:
        :return:
        """
        rank = self.recommendate(user, train, k)
        return sorted(rank.items(), key=lambda x: x[1], reverse=True)[0:N]

    def precision(self, train, test, N, k):
        hit = 0
        all = 0
        for user in train.keys():
            if user in test:  # 保证测试集存在
                tu = test[user]
                rank = self.getRecommendation(user, train, N, k)
                for item, pui in rank:
                    if item in tu:
                        hit += 1
                all += N
        return hit / (all * 1.0)

    def recall(self, train, test, N, k):
        hit = 0
        all = 0
        for user in train.keys():
            if user in test:  # 保证测试集存在
                tu = test[user]
                rank = self.getRecommendation(user, train, N, k)
                for item, pui in rank:
                    if item in tu:
                        hit += 1
                all += len(tu)
        return hit / (all * 1.0)

class ItemItemRecommendation():
    """
    based on item recommendation.
    """
    def __init__(self):
        self.W = None  # W[u][v] is the similarity between u and v

    def save(self, file="item_item_model"):
        cPickle.dump(self.W, open(file, "wb"))

    def load(self, file="item_item_model"):
        self.W = cPickle.load(open(file, "rb"))

    def itemSimilarity(self, train):
        # calculate co-rated users between items
        C = dict()
        N = dict()
        for u, items in train.items():
            for i in items:
                if i not in N:
                    N[i] = 0
                N[i] += 1
                if i not in C:
                    C[i] = dict()
                for j in items:
                    if i == j:
                        continue
                    if j not in C[i]:
                        C[i][j] = 0
                    C[i][j] += 1
        W = dict()
        for i, related_items in C.items():
            if i not in W:
                W[i] = dict()
            for j, cij in related_items.items():
                W[i][j] = cij / math.sqrt(N[i] * N[j])
        self.W = W

    def recommendation(self, user, train, k):
        rank = dict()
        ru = train[user]
        for i, pi in ru.items():
            k_item_smi = sorted(self.W[i].items(), key=lambda x: x[1], reverse=True)[0:k]
            for j, wj in k_item_smi:
                if j in ru:
                    continue
                if j not in rank:
                    rank[j] = 0
                rank[j] += pi * wj
        return rank

    def getRecommendation(self, user, train, N, k):
        rank = self.recommendation(user, train, k)
        return sorted(rank.items(), key=lambda x: x[1], reverse=True)[0:N]

    def precision(self, train, test, N, k):
        hit = 0
        all = 0
        for user in train.keys():
            print "success"
            if user in test:  # 保证测试集存在
                tu = test[user]
                rank = self.getRecommendation(user, train, N, k)
                for item, pui in rank:
                    if item in tu:
                        hit += 1
                all += N
        return hit / (all * 1.0)

    def recall(self, train, test, N, k):
        hit = 0
        all = 0
        for user in train.keys():
            if user in test:  # 保证测试集存在
                tu = test[user]
                rank = self.getRecommendation(user, train, N, k)
                for item, pui in rank:
                    if item in tu:
                        hit += 1
                all += len(tu)
        return hit / (all * 1.0)

def splitData(data, M, k, seed):
    test = []
    train = []
    random.seed(seed)
    for user, item, score in data:
        if random.randint(0,M)==k:
            test.append([user, item, score])
        else:
            train.append([user, item, score])
    return train, test


if __name__ == '__main__':
    with open("ml-1m/ratings.dat", "r") as f:
        lines = f.readlines()
    lines = map(lambda line: line.strip(), lines)
    datas = []
    for line in lines:
        d = line.split("::")[0:3]
        datas.append([int(d[0]), int(d[1]), 1])
    data = datas
    M = 20
    k = 10
    seed = 1
    train, test = splitData(data, M, k, seed)
    train_dict = {}  # user_id {item_id:score}
    test_dict = {}
    for user, item, score in train:
        if user not in train_dict:
            train_dict[user] = {}
        train_dict[user][item] = score
    for user, item, score in test:
        if user not in test_dict:
            test_dict[user] = {}
        test_dict[user][item] = score
    # ItemItemRecommendation
    model = ItemItemRecommendation()
    model.load()
    model.recall(train_dict, test_dict, 10, 100)