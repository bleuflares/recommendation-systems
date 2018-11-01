import sys
import numpy as np
import math

#predicted rating
def predict(x, y):
    val = np.sum(x * y)
    if val > 5.0:
        val = 5.0
    if val < 1.0:
        val = 1.0
    return val

# train for single k by calculating prediction and train U and V by adding proportional to error
def train(U, V, max_user, max_item, k, ratings, lr=0.02, reg=0.05):
    sse = 0.0
    count = 0
    for i in range(max_user):
        for j in range(max_item):
            rating = ratings[i][j]
            if rating != 0:
                err = rating - predict(U[i], np.transpose(V[:, j]))
                sse += err ** 2
                count += 1
                utemp = U[i][k]
                vtemp = V[k][j]
                U[i][k] += lr * (err * vtemp - reg * utemp)
                V[k][j] += lr * (err * utemp - reg * vtemp)
    return (U, V, math.sqrt(sse / count))

#train each k for multiple epoch until the erro does not change much
def trainall(U, V, ratings, maxepoch, threshold):
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

#train U, V
def get_UV(ratings, max_user, max_item, avg_rating, feat):
    uv_init = math.sqrt(avg_rating / feat)

    U = np.full((max_user, feat), uv_init)
    V = np.full((feat, max_item), uv_init)

    U, V = trainall(U, V, ratings, 10, 0.05) #input a normalized rating or original rating?
    return (U, V)

if __name__ == "__main__":

#read input, store user-item-rating and item-time-rating
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

    #fill rating array and calculate avg rating
    ratings = np.zeros((max_user, max_item))
    avg_rating = 0
    for point in points:
        ratings[user_sets_list.index(point[0]) - 2][item_sets_list.index(point[1])] = point[2]
        avg_rating += point[2]
    avg_rating = avg_rating / len(points)

    #later used for movies that does not exist in V
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
    """
    normalized_ratings = np.zeros((max_user, max_item))
    for i in range(max_user):
        for j in range(max_item):
            if ratings[i][j] != 0:
                normalized_ratings[i][j] = ratings[i][j] - user_means[i]
    """

    #record a time rating of each movies
    time_ratings = []
    for i in range(len(item_sets_list)):
        time_rating = []
        for point in time_points:
            if item_sets_list[i] == point[1]:
                time_rating.append((point[0], point[2]))
        time_ratings.append(time_rating)

    #calculate the average of change in rating along the time for each movie
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

    #normalize the margin
    for i in range(max_item):
        if trending_margin[i] != 0:
            trending_margin[i] = trending_margin[i] - margin_mean

    #finished with input processing
    input_file.close()


    #get the U, V approximate
    U, V = get_UV(ratings, max_user, max_item, avg_rating, 10)
    mat = np.matmul(U, V)

    test_file = open(sys.argv[2], 'r')
    output_file = open("output.txt", 'w')
    weight = 1.0
    #rmse = 0.0
    #count = 0
    #apply time margin and write output
    for line in test_file:
        time_margin = 0
        point = line.split(',')
        if int(point[1]) in item_sets_list:
            i = item_sets_list.index(int(point[1]))
            for j in range(len(time_ratings[i]) - 1): #find the position of timestamp
                if time_ratings[i][j][0] <= int(point[3]) <= time_ratings[i][j + 1][0]:
                    time_margin = trending_margin[i] * j / (len(time_ratings[i]) - 1) #calculate time margin
                    break
            prediction = np.mean(mat[:, i]) + weight * time_margin #calculate prediction
            #boundary check
            if prediction > 5.0:
                prediction = 5.0
            if prediction < 1.0:
                prediction = 1.0
        elif int(point[0]) in user_sets_list:
            prediction = user_means[user_sets_list.index(int(point[0]))]
        else:
            prediction = avg_rating
        output_file.write(','.join([str(point[0]), str(point[1]), str(prediction), str(point[3])]))
    output_file.close()
    test_file.close()
