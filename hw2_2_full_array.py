import sys
import numpy as np
import math

if __name__ == "__main__":
	input_file = open(sys.argv[1], 'r')

	max_user = 0
	max_item = 0

	points = []

	for line in input_file:
		point = line.split(',')
		if max_user < int(point[0]):
			max_user = int(point[0])
		if max_item < int(point[1]):
			max_item = int(point[1])
		points.append([int(point[0]), int(point[1]), float(point[2])])

	item_sets_list = list(item_sets)
	max_1000 = 0
	for i in range(1000):
		if i in item_sets_list:
			if i > max_1000:
				max_1000 = i
	max_idx = item_sets_list.index(max_1000)
	print(max_idx)

	ratings = np.zeros((max_user, max_item))

	for point in points:
		ratings[point[0] - 2][point[1] - 1] = point[2]

	user_means = np.zeros(max_user)
	for i in range(max_user):
		user_means = ratings.mean(axis = 0)

	normalized_ratings = np.zeros((max_user, max_item))
	for i in range(max_user):
		for j in range(max_item):
			if ratings[i][j] != 0:
				normalized_ratings[i][j] = ratings[i][j] - user_means[i]

	def cosine_distance(arr1, arr2):
		dot = 0
		length1 = 0
		length2 = 0
		for i in range(arr1.size):
			dot = dot + arr1[i] * arr2[i]
			length1 = length1 + arr1[i] * arr1[i]
			length2 = length2 + arr2[i] * arr2[i]
		if length1 == 0 or length2 == 0:
			return 99999999
		else:
			return 1- dot / (math.sqrt(length1) * math.sqrt(length2))

	user_distances = np.zeros(max_user)

	for i in range(max_user):
		if i != 598:
			user_distances[i] = cosine_distance(normalized_ratings[598], normalized_ratings[i])
	user_distances[598] = 99999999

	user_max_idx = np.argsort(user_distances)[:10]
	predicted_user_ratings = np.zeros(max_idx + 1)

	for j in range(max_idx + 1):
		rating_sum = 0
		count = 0
		for i in range(10):
			rating = ratings[user_max_idx[i]][j]
			print(rating)
			if rating != 0:
				rating_sum = rating_sum + rating
				count = count + 1
		predicted_user_ratings[j] = rating_sum / count

	top5_user_indices = np.argsort(predicted_user_ratings)[-5:]

	for i in range(5):
		print(predicted_user_ratings[top5_user_indices[i]])

	print("user calc fin")

	min_10_indices = []
	for i in range(max_idx + 1):
		item_distances = []
		item_indices = []
		for j in range(max_item):
			if i != j and ratings[598][j] != 0:
				item_distances.append(cosine_distance(ratings[:, i], ratings[:, j]))
				item_indices.append(j)
		min_10 = sorted(range(len(item_distances)), key=lambda i: item_distances[i])[:10]
		min_10_idx = []
		for k in min_10:
			min_10_idx.append(item_indices[k])
		min_10_indices.append(min_10_idx)

	predicted_item_ratings = np.zeros(max_idx + 1)
	for i in range(max_idx + 1):
		count = 0
		rating_sum = 0
		for j in range(len(min_10_indices[i])):
			rating = ratings[598][min_10_indices[i][j]]
			if rating != 0:
				rating_sum += rating
				count += 1
		predicted_item_ratings[i] = rating_sum / count

	top5_item_indices = np.argsort(predicted_item_ratings)[-5:]

	for i in range(5):
		print(predicted_item_ratings[top5_item_indices[i]])
	
