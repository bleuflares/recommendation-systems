import sys
import numpy as np
import math

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
	#print(ratings[0])

	user_means = np.zeros(max_user)
	for i in range(max_user):
		user_means = ratings.mean(axis = 1)

	normalized_ratings = np.zeros((max_user, max_item))
	for i in range(max_user):
		for j in range(max_item):
			if ratings[i][j] != 0:
				normalized_ratings[i][j] = ratings[i][j] - user_means[i]

	def cosine_distance(arr1, arr2):
		dot = np.sum(arr1 * arr2)
		length1 = np.sum(arr1 * arr1)
		length2 = np.sum(arr2 * arr2)
		if length1 == 0 or length2 == 0:
			return 99999999
		else:
			return 1 - dot / (math.sqrt(length1) * math.sqrt(length2))

	user_distances = np.zeros(max_user)

	for i in range(max_user):
		if i != 598:
			user_distances[i] = cosine_distance(normalized_ratings[598], normalized_ratings[i])
	user_distances[598] = 99999999

	print("user dist calc fin")

	min_10_indices = []
	for i in range(max_idx + 1):
		item_distances = []
		item_indices = []
		for j in range(max_item):
			if i != j: # and ratings[598][j] != 0 ?? should I add it or not?
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
		
		#if and ratings[598][j] != 0  used in upper for, if count ==0 not needed
		if count == 0:
			predicted_item_ratings[i] = 0
		else:
			predicted_item_ratings[i] = rating_sum / count

	top5_item_indices = np.argsort(predicted_item_ratings)[-5:]
	print(top5_item_indices)

	for i in range(5):
		print(predicted_item_ratings[top5_item_indices[i]])
	"""
	user_min_10 = np.argpartition(user_distances, 10)[:10]
	print("unsorted")
	print(user_distances[user_min_10])
	user_idx = user_min_10[np.argsort(user_distances[user_min_10])]
	
	print("similar users are")
	print(user_idx)
	"""

	user_min_10 = np.argsort(user_distances)[:10]
	
	print("user_min idx and distances")
	print(user_min_10)
	print(user_distances[user_min_10])

	predicted_user_ratings = np.zeros(max_idx + 1)
	for j in range(max_idx + 1):
		rating_sum = 0
		count = 0
		for i in range(10):
			rating = ratings[user_min_10[i]][j]
			if rating != 0:
				rating_sum = rating_sum + rating
				count = count + 1
		if count == 0:
			predicted_user_ratings[j] = 0
		else:
			predicted_user_ratings[j] = rating_sum / count

	top5_user_indices = np.argsort(predicted_user_ratings)[-5:]
	print(top5_user_indices)

	for i in range(5):
		print(predicted_user_ratings[top5_user_indices[i]]) # need to match with real movie number