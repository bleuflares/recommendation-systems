import sys
import numpy as np
import math

if __name__ == "__main__":
	train_file = open(sys.argv[1], 'r')
	test_file = open(sys.argv[2], 'rw')
	max_user = 0
	max_item = 0

	points = []

	for line in train_file:
		point = line.split(',')
		if max_user < int(point[0]):
			max_user = int(point[0])
		if max_item < int(point[1]):
			max_item = int(point[1])
		points.append([int(point[0]), int(point[1]), float(point[2])])

	ratings = np.zeros((max_user, max_item))

	user_means = np.zeros(max_user)
	for i in range(max_user):
		user_means = ratings.mean(axis = 1)

	for point in points:
		ratings[point[0] - 1][point[1] - 1] = point[2]

	print("max user is", max_user)
	print("max item is", max_item)

	normalized_ratings = np.zeros((max_user, max_item))
	for i in range(max_user):
		for j in range(max_item):
			if ratings[i][j] != 0:
				normalized_ratings[i][j] = ratings[i][j] - user_means[i]

	def cosine_distance(arr1, arr2):
		dot = arr1 * arr2
		length1 = arr1 * arr1
		length2 = arr2 * arr2
		if length1 == 0 or length2 == 0:
			return 99999999
		else:
			return dot / (math.sqrt(length1) * math.sqrt(length2))