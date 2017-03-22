simple personality recommendation system: recommedation based on item and user
author:zhangluoyang email:55058629@qq.com
environment dependence
python2.7
cPick
datasets: https://grouplens.org/datasets/movielens/
this is a simple example, attend to comprehension the two algoriths for recommendation.
there are two recommendation model(class) in this programe, UserItemRecommendation and ItemItemRecommendation.
each model hava indispensable functions:
    1 userSimilarity: calculate similarity between users or items.
    2 save: save the trained model
    3 load: load the exists model from local system.
    4 precision: calculate the precision rate based on test data
    5 recall: calculate the recall rate based on test data
    6 getRecommendation: get the recommendation result based on the test data.
you can just run this example by: python recommendation.py
reference:
    1 推荐系统实践
