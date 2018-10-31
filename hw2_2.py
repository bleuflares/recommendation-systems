import sys
import numpy as np
import math

#cosine distance function
def cosine_distance(arr1, arr2):
	dot = np.sum(np.dot(arr1, arr2))
	length1 = np.sum(np.dot(arr1, arr1))
	length2 = np.sum(np.dot(arr2, arr2))
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

	#remove sparcity
	max_user = len(user_sets)
	max_item = len(item_sets)

	#list of movie ids
	item_sets_list = sorted(list(item_sets))

	#find the index of max among 1000
	max_1000 = 0
	for i in range(1000):
		if i in item_sets_list:
			if i > max_1000:
				max_1000 = i
	max_idx = item_sets_list.index(max_1000) + 1
	

	#create, fill the ratings matrix
	ratings = np.zeros((max_user, max_item))
	for point in points:
		ratings[point[0] - 2][item_sets_list.index(point[1])] = point[2]

	#find the mean rating of each user
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

	#normalizeed ratings array
	normalized_ratings = np.zeros((max_user, max_item))
	for i in range(max_user):
		for j in range(max_item):
			if ratings[i][j] != 0:
				normalized_ratings[i][j] = ratings[i][j] - user_means[i]

	#find 10 users with minimum cosine distance
	user_distances = np.zeros(max_user)
	for i in range(max_user):
		if i != 598:
			user_distances[i] = cosine_distance(normalized_ratings[598], normalized_ratings[i])
	user_distances[598] = 99999999

	user_min_10 = np.argsort(user_distances)[:10]

	#predicted rating for movie 1 ~ 1000 for user-based approach
	predicted_user_ratings = np.zeros(max_idx)
	for j in range(max_idx):
		rating_sum = 0
		count = 0
		for i in range(len(user_min_10)):
			rating = normalized_ratings[user_min_10[i]][j]
			if rating != 0:
				rating_sum = rating_sum + rating
				count = count + 1
		if count == 0:
			predicted_user_ratings[j] = 0
		else:
			predicted_user_ratings[j] = rating_sum / count
	#get the index of top 5 rated movies
	top5_user_indices = np.argsort(predicted_user_ratings)[-5:][::-1]

	#retreive actual movie id and print
	for i in range(len(top5_user_indices)):
		print("%d\t%f" %(item_sets_list[top5_user_indices[i]], predicted_user_ratings[top5_user_indices[i]] + user_means[598]))

	#get the index of 10 similar movies to each of 1 ~ 1000
	min_10_indices = []
	for i in range(max_idx):
		item_distances = []
		item_indices = []
		for j in range(max_item):
			if i != j:
				item_distances.append(cosine_distance(normalized_ratings[:, i], normalized_ratings[:, j]))
				item_indices.append(j)
		min_10 = sorted(range(len(item_distances)), key=lambda i: item_distances[i])[:10]
		min_10_idx = []
		for k in min_10:
			min_10_idx.append(item_indices[k])
		min_10_indices.append(min_10_idx)
		#min_10_indices[i] is a list of indices where 10 min distances appear for item i

	#predicted rating for movie 1 ~ 1000 for user-based approach
	predicted_item_ratings = np.zeros(max_idx)
	for i in range(max_idx):
		count = 0
		rating_sum = 0
		for j in range(len(min_10_indices[i])):
			rating = ratings[598][min_10_indices[i][j]]
			if rating != 0:
				rating_sum += rating
				count += 1
		if count == 0:
			predicted_item_ratings[i] = 0
		else:
			predicted_item_ratings[i] = rating_sum / count

	#get the index of top 5 rated movies
	top5_item_indices = np.argsort(predicted_item_ratings)[-5:][::-1]

	#retreive actual movie id and print
	for i in range(len(top5_item_indices)):
		print("%d\t%f" %(item_sets_list[top5_item_indices[i]], predicted_item_ratings[top5_item_indices[i]]))