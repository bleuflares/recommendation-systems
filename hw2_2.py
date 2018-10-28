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

	ratings = np.zeros((max_user, max_item))

	for point in points:
		ratings[point[0] - 1][point[1] - 1] = point[2]

	user_means = np.zeros(max_user)
	for i in range(max_user):
		user_means = ratings.mean(axis = 0)

	normalized_ratings = np.zeros((max_user, max_item))
	for i in range(max_user):
		for j in range(max_item):
			if ratings[i][j] != 0:
				normalized_ratings[i][j] = ratings[i][j] - user_means[i]

		"""
		user_means = np.full((1, y), ratings.mean(ratings[i, :]))

		for i in range(x - 1):
			user_means = np.concatenate(user_means, np.full((1, y), ratings.mean(ratings[i + 1, :])))
		
		normalized_ratings = ratings - user_means
		"""

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
			return dot / (math.sqrt(length1) * math.sqrt(length2))

	user_distances = np.zeros(max_user)

	for i in range(max_user):
		if i != 599:
			user_distances[i] = cosine_distance(normalized_ratings[599], normalized_ratings[i])
	user_distances[599] = 99999999

	print("user dist calc fin")

	min_10_indices = []
	for i in range(1000):
		item_distances = []
		item_indices = []
		for j in range(max_item):
			if i != j and ratings[599][j] != 0:
				item_distances.append(cosine_distance(ratings[:, i], ratings[:, j]))
				item_indices.append(j)
		min_10 = sorted(range(len(item_distances)), key=lambda i: item_distances[i])[:10]
		min_10_idx = []
		for k in min_10:
			min_10_idx.append(item_indices[k])
		min_10_indices.append(min_10_idx)

	print("item dist calc fin")
	"""
	item_idx = np.argpartition(item_distances[0], 10)[10:]
	item_max_idx = item_idx[np.argsort(item_distances[item_idx])]
	for i in range(999):
		item_idx = np.argpartition(item_distances[i], 10)[10:]
		item_max_idx = np.concatenate(item_max_idx, item_idx[np.argsort(item_distances[item_idx])])

	print("max item found")
	"""

	predicted_item_ratings = np.zeros(1000)
	for i in range(1000):
		count = 0
		rating_sum = 0
		for j in range(len(min_10_indices[i])):
			rating = ratings[599][min_10_indices[i][j]]
			if rating != 0:
				rating_sum += rating
				count += 1
		predicted_item_ratings[i] = rating_sum / count

	top5_item_indices = np.argsort(predicted_item_ratings)[-5:]

	for i in range(5):
		print(predicted_item_ratings[top5_item_indices[i]])
		print("predict item got")
	
	user_idx = np.argpartition(user_distances, 10)[10:]
	user_max_idx = user_idx[np.argsort(user_distances[user_idx])]

	print("max user found")
	
	predicted_user_ratings = np.zeros(1000)
	for j in range(1000):
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
		print("predict user got")