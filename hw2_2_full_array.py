import sys
import numpy as np
import math

if __name__ == "__main__":
	input_file = open(sys.argv[1], 'r')

	max_user = 0
	max_item = 0
	item_sets = set()

	points = []

	for line in input_file:
		point = line.split(',')
		item_sets.add(int(point[1]))
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
	max_idx = item_sets_list.index(max_1000) + 1

	max_user = max_user - 1
	#find the max index of the item less than 1000
	print(max_idx)
	print(max_user)
	print(max_item)

	ratings = np.zeros((max_user, max_item))

	for point in points:
		ratings[point[0] - 2][point[1] - 1] = point[2] #user 1 does not exist, start from 2, user 2 goes to row 0 movie 1 goes to col 0

	user_means = np.zeros(max_user)
	for i in range(max_user):
		user_means = ratings.mean(axis = 0)

	normalized_ratings = np.zeros((max_user, max_item))
	for i in range(max_user):
		for j in range(max_item):
			if ratings[i][j] != 0:
				normalized_ratings[i][j] = ratings[i][j] - user_means[i] #normalize rating by subtracting the row sum

	def cosine_distance(arr1, arr2): # cosine distance btw two arrays
		dot = np.sum(arr1 * arr2)
		length1 = np.sum(arr1 * arr1)
		length2 = np.sum(arr2 * arr2)
		if length1 == 0 or length2 == 0: #infinite distance if length is 0
			return 99999999
		else:
			return 1 - dot / (math.sqrt(length1) * math.sqrt(length2)) # cosine distance = 1-cosine similarity

	user_distances = np.zeros(max_user)
	for i in range(max_user):
		if i != 598: #598 is the user id 600
			user_distances[i] = cosine_distance(normalized_ratings[598], normalized_ratings[i]) #calculate cosine distance btw user 600 and others
	user_distances[598] = 99999999 # make the distance of itself as infinite
	user_max_idx = np.argsort(user_distances)[:10] #get users with min 10 distances
	
	# get the average rating of min distance users for each 1 ~ 1000 movie
	predicted_user_ratings = np.zeros(max_idx)
	for j in range(max_idx):
		rating_sum = 0
		count = 0
		for i in range(10):
			rating = ratings[user_max_idx[i]][j]
			if rating != 0:
				rating_sum = rating_sum + rating
				count = count + 1
		if count == 0: #rate 0 to exclude if no one rated
			predicted_user_ratings[j] = 0
		else:
			predicted_user_ratings[j] = rating_sum / count

	top5_user_indices = np.argsort(predicted_user_ratings)[-5:][::-1] #get the index top 5 ratings

	for i in range(len(top5_user_indices)):
		print(top5_user_indices[i])#index of movies rated as top 5
		print(item_sets_list[top5_user_indices[i]]) # id of the movie with the index
		print(predicted_user_ratings[top5_user_indices[i]]) # top 5 ratings

	min_10_indices = []
	for i in range(max_idx):
		item_distances = []
		item_indices = []
		for j in range(max_item):
			if i != j:# and ratings[598][j] != 0:
				item_distances.append(cosine_distance(ratings[:, i], ratings[:, j]))
				item_indices.append(j)
		min_10 = sorted(range(len(item_distances)), key=lambda i: item_distances[i])[:10]
		min_10_idx = []
		for k in min_10:
			min_10_idx.append(item_indices[k])
		min_10_indices.append(min_10_idx)

	predicted_item_ratings = np.zeros(max_idx)
	for i in range(max_idx):
		count = 0
		rating_sum = 0
		for j in range(len(min_10_indices[i])):
			rating = ratings[598][min_10_indices[i][j]]
			if rating != 0:
				rating_sum += rating
				count += 1
		predicted_item_ratings[i] = rating_sum / count

	top5_item_indices = np.argsort(predicted_item_ratings)[-5:][::-1]

	for i in range(5):
		print(predicted_item_ratings[top5_item_indices[i]])
	
