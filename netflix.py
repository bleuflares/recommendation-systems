import sys
import numpy as np
import math


def cosine_distance(arr1, arr2):
    dot = np.sum(arr1 * arr2)
    length1 = np.sum(arr1 * arr1)
    length2 = np.sum(arr2 * arr2)
    if length1 == 0 or length2 == 0:
        return 99999999
    else:
        return 1 - dot / (math.sqrt(length1) * math.sqrt(length2))

def predict(x, y):
    val = np.sum(x * y)
    if val > 5:
        val = 5
    if val < 1:
        val = 1
    return val

def train(U, V, max_user, max_item, k, ratings, lrate=0.02, regularizer=0.02):
    sse = 0.0
    n = 0
    # get current rating
    for i in range(max_user):
        for j in range(max_item):
            rating = ratings[i][j]
            if rating != 0:
                err = rating - predict(U[i], np.transpose(V[:, j]))
                sse += err**2
                n += 1
                uTemp = U[i][k]
                vTemp = V[k][j]
                U[i][k] += lrate * (err * vTemp - regularizer * uTemp)
                V[k][j] += lrate * (err * uTemp - regularizer * vTemp)
    return (U, V, math.sqrt(sse / n))

def trainall(U, V, ratings, maxepoch, threshold):
    # stub -- initial train error
    prevtrainerr = 1000000.0
    max_user, feat = U.shape
    _, max_item = V.shape
    for k in range(feat):
        for epoch in range(maxepoch):
            U, V, trainerr = train(U, V, max_user, max_item, k, ratings)
            if abs(prevtrainerr - trainerr) < threshold:
                break
            prevtrainerr = trainerr
    return U, V

def get_UV(ratings, max_user, max_item, avg_rating, feat):

    uv_init = math.sqrt(avg_rating / feat)
    print(uv_init)

    U = np.full((max_user, feat), uv_init)
    V = np.full((feat, max_item), uv_init)

    U, V = trainall(U, V, ratings, 10, 0.05) #input a normalized rating or original rating?
    return (U, V)

if __name__ == "__main__":

    input_file = open(sys.argv[1], 'r')
    user_sets = set()
    item_sets = set()
    points = []
    time_points = []
    for line in input_file:
        point = line.split(',')
        user_sets.add(int(point[0]))
        item_sets.add(int(point[1]))
        points.append([int(point[0]), int(point[1]), float(point[2])])
        time_points.append([int(point[3]), int(point[1]), float(point[2])])
    
    time_points.sort(key=lambda arr: arr[0])
    user_sets_list = sorted(list(user_sets))
    item_sets_list = sorted(list(item_sets))

    max_user = len(user_sets_list)
    max_item = len(item_sets_list)
    print("max user is", max_user)
    print("max item is", max_item)

    ratings = np.zeros((max_user, max_item))
    avg_rating = 0
    for point in points:
        ratings[user_sets_list.index(point[0]) - 2][item_sets_list.index(point[1])] = point[2]
        avg_rating += point[2]
    avg_rating = avg_rating / len(points)
    print("avg rating fin")

    """
    user_means = []
    for i in range(max_user):
        user_mean = 0
        user_count = 0
        for j in range(max_item):
            if ratings[i][j] != 0:
                user_mean += ratings[i][j]
                user_count += 1
        if user_count > 0:
            user_means.append(user_mean / user_count)
        else:
            user_means.append(0)
    
    normalized_ratings = np.zeros((max_user, max_item))
    for i in range(max_user):
        for j in range(max_item):
            if ratings[i][j] != 0:
                normalized_ratings[i][j] = ratings[i][j] - user_means[i]
    """

    time_ratings = []
    for i in range(len(item_sets_list)):
        time_rating = []
        for point in time_points:
            if item_sets_list[i] == point[1]:
                time_rating.append((point[0], point[2]))
        time_ratings.append(time_rating)
    print("timerating fin")

    trending_margin = []
    for i in range(max_item):
        time_rating = time_ratings[i]
        item_margin = 0
        if len(time_rating) > 1:
            for j in range(len(time_rating) - 1):
                item_margin += (time_rating[j][1] - time_rating[j + 1][1])
            trending_margin.append(item_margin / (len(time_rating) - 1))
        else:
            trending_margin.append(0)

    margin_mean = 0
    count = 0
    for i in range(max_item):
        if trending_margin[i] != 0:
            margin_mean += trending_margin[i]
            count += 1
    margin_mean = margin_mean / count

    for i in range(max_item):
        if trending_margin[i] != 0:
            trending_margin[i] = trending_margin[i] - margin_mean
    print("trending_margin fin")
    

    #finished with input processing

    U, V = get_UV(ratings, max_user, max_item, avg_rating, 10)
    mat = np.matmul(U, V)
    #print(mat)

    output_file = open(sys.argv[2], 'r')
    weight = 1.0
    rmse = 0.0
    count = 0
    for line in output_file:
        time_margin = 0
        point = line.split(',')
        if int(point[1]) in item_sets_list:
            i = item_sets_list.index(int(point[1]))
            for j in range(len(time_ratings[i]) - 1):
                if time_ratings[i][j][0] <= int(point[3]) <= time_ratings[i][j + 1][0]:
                    #time_margin = (time_ratings[i][j][1] + time_ratings[i][j + 1][1]) / 2
                    time_margin = trending_margin[i] * j / (len(time_ratings[i]) - 1)
                    break
            prediction = np.mean(mat[:, i]) + weight * time_margin
            if prediction > 5:
                prediction = 5
            if prediction < 1:
                prediction = 1
            err = (prediction - float(point[2]))
            #print("mat mean: %f time_margin:%f, rating: %f, err: %f" %(np.mean(mat[:, i]), time_margin, float(point[2]), err))
            rmse += err**2
            count += 1

    print(math.sqrt(rmse / count))

"""
regression code
weight = 1.0
    lr = 0.01
    prevrmse = 0.8

    output_file = open(sys.argv[2], 'r')
    rmse = 0.0
    count = 0
    no_count = 0

    #0:time 1: id 2: rating
    for point in test_points:
        time_margin = 0
        if int(point[1]) in item_sets_list:
            i = item_sets_list.index(point[1])
            for j in range(len(time_ratings[i]) - 1):
                if time_ratings[i][j][0] <= point[0] <= time_ratings[i][j + 1][0]:
                    #time_margin = (time_ratings[i][j][1] + time_ratings[i][j + 1][1]) / 2
                    time_margin = trending_margin[i] * j / (len(time_ratings[i]) - 1)
                    break
            prediction = np.mean(mat[:, i]) + weight * time_margin
            if prediction > 5:
                prediction = 5
            if prediction < 1:
                prediction = 1
            err = (prediction - point[2])
            #print("mat mean: %f time_margin:%f, rating: %f, err: %f" %(np.mean(mat[:, i]), time_margin, float(point[2]), err))
            rmse += err**2
            count += 1
        else:
            no_count += 1
    print(math.sqrt(rmse / count))
"""


#weight computition code
"""
        U, V = get_UV(ratings, user_sets_list, item_sets_list, avg_rating, 10)
    mat = np.matmul(U, V)
    print(mat)
    output_file = open(sys.argv[2], 'r')

    rmse_thrs = 0.01
    prevrmse = 1.2
    weight = 0.5
    lr = 0.01

    test_points = []
    for line in output_file:
        point = line.split(',')
        test_points.append(point)
        time_margin = 0

    for i in range(maxepoch_):
        sqerrsum = 0.0
        count = 0
        for point in test_points:
            #print(point[1])
            if point[1] in item_sets_list:
                print(point[1])
                i = item_sets_list.index(point[1])
                for j in range(len(time_ratings[i]) - 1):
                    if time_ratings[i][j][0] <= point[3] <= time_ratings[i][j + 1][0]:
                        time_margin = (time_ratings[i][j][1] + time_ratings[i][j + 1][1]) / 2
                err = ((np.mean(mat[:, i]) * weight + time_margin * (1 - weight)) - point[2])
                sqerrsum += err**2
                count += 1

        rmse = math.sqrt(sqerrsum / count)
        print("epoch %d rmse %f" %(i, rmse))
        if abs(prevrmse - rmse) < rmse_thrs:
            break
        weight = weight + lr
        print("weight %f" %weight)
        prevrmse = rmse
    """

#output code
"""
    output = open("output.txt", 'r')
    for line in output_file:
        time_margin = 0
        point = line.split(',')
        i = item_sets_list.index(point[1])
        for j in range(len(time_ratings[i]) - 1):
            if time_ratings[i][j][0] <= point[3] <= time_ratings[i][j + 1][0]:
                time_margin = (time_ratings[i][j][1] + time_ratings[i][j + 1][1]) / 2

        point[2] = (mat[point[0]][point[1]] + time_margin) / 2
        output.write(','.join(point) + "\n")
"""

#margin code may use or not
"""
    trending_margin = np.array(max_item)
    for i in range(max_item):
        item_row = trending[i]
        item_margin = 0
        for j in range(999):
            if item_row[j + 1] == 0:
                break
            item_margin += (item_row[j] - item_row[j + 1])
        trending_margin[i] = item_margin

    margin_mean = np.mean(trending_margin)
"""