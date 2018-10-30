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

if __name__ == "__main__":

	input_file = open(sys.argv[1], 'r')

	points = []
	user_sets = set()
	item_sets = set()

	for line in input_file:
		point = line.split(',')
		user_sets.add(int(point[0]))
		item_sets.add(int(point[1]))
		points.append([int(point[0]), int(point[1]), float(point[2])])

	#user 1 does not exist starts from 2
	max_user = len(user_sets)
	max_item = len(item_sets)

	items_indices = list(item_sets)
	max_idx = 0
	for i in range(1000):
		if i in items_indices:
			if i > max_idx:
				max_idx = i
	print(max_idx)
	print(items_indices.index(max_idx))
	
	ratings = np.zeros((max_user, max_item))

	for point in points:
		ratings[point[0] - 2][items_indices.index(point[1])] = point[2]

	print("max user is", max_user)
	print("max item is", max_item)

	user_means = np.zeros(max_user)
	for i in range(max_user):
		user_means = ratings.mean(axis = 1)

	normalized_ratings = np.zeros((max_user, max_item))
	for i in range(max_user):
		for j in range(max_item):
			if ratings[i][j] != 0:
				normalized_ratings[i][j] = ratings[i][j] - user_means[i]

	total_avg = user_means.mean()

	U = np.full((max_user, feat), total_avg)
	V = np.full((feat, max_item), total_avg)

	def predict(i, j):
		val = np.sum((U[i] * np.transpose(V[:, j])))
		if val > 5:
			val = 5
		if val < 1:
			val = 1
		return val

	def train(k):
        sse = 0.0
        n = 0
        # get current rating
        for i in range(max_user):
        	for j in range(max_item):
            	rating = ratings[i][j]
            	err = rating - predict(i, j)
            	sse += err**2
            	n += 1

        		uTemp = U[i][k]
        		vTemp = V[k][j]

            	U[i][k] += lrate * (err * vTemp - regularizer * uTemp)
            	V[k][j] += lrate * (err * uTemp - regularizer * vTemp)
        return math.sqrt(sse / n)

    def trainall(feat, maxepoch):        
        # stub -- initial train error
        prevtrainerr = 1000000.0
        for k in range(feat):
            for epoch in range(maxepoch):
                trainerr = train(U, V, k)
                if abs(oldtrainerr - trainerr) < threshold:
                    break
                prevtrainerr = trainerr