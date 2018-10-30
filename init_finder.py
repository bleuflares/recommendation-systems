import sys
import numpy as np
import math
from pyspark import SparkConf, SparkContext

def distance(arr1, arr2): #Euclidean distance
	dist = 0
	for i in range(len(arr1)):
		dist += (arr1[i] - arr2[i]) * (arr1[i] - arr2[i])
	return (dist)

if __name__ == "__main__":
	input_file = open(sys.argv[1], 'r')
	k = int(sys.argv[2])
	points = [] #list of float coordinates
	k_means = [] #list of clusteroids
	k_means_indices = [] #index of cluseroids in points

	for line in input_file:
		point = line.split()
		float_point = []
		for p in point:
			float_point.append(float(p))
		points.append(float_point)

	distances = np.zeros((len(points), len(points))) #distance matrix for calculating distance btw all points
	
	k_means.append(points[0]) #first random point is points[0]
	k_means_indices.append(0)
	k_means_exclude = list(set(range(len(points))) - set(k_means_indices)) #non-clusteroid points

	if k > 1:
		for i in range(len(points)): #calculate distance btw points
			for j in range(len(points)):
				distances[i, j] = distance(points[i], points[j])
		while(len(k_means) < k): #while there are fewer than k points
			row_idx = np.array(k_means_indices) #row is selected points
			col_idx = np.array(k_means_exclude)
			a = distances[row_idx, col_idx] # ditance from selected points to non-selected ones
			x, y = np.unravel_index(np.argmax(a, axis=None), a.shape) #get the index with max distance
			k_means.append(points[y])
			k_means_indices.append(y)
			k_means_exclude = list(set(range(len(points))) - set(k_means_indices))

	input_file.close()

	def k_means_distance(arr):
		min_dist = 9999999999
		min_point = None
		for point in k_means:
			dist = distance(point, arr)
			if dist < min_dist:
				min_dist = dist
				min_point = point
		return (k_means.index(min_point), [arr])

	def max_distance(pair):
		max_dist = 0
		for i in pair[1]:
			for j in pair[1]:
				dist = distance(i, j)
				if max_dist < dist:
					max_dist = dist
		return (pair[0], max_dist)

	conf = SparkConf()
	sc = SparkContext(conf=conf)
	lines = sc.parallelize(points)
	centroids_map = lines.map(k_means_distance)
	clusters = centroids_map.reduceByKey(lambda a, b: a + b)
	diameters = clusters.map(max_distance).collect()
	
	diameter_sum = 0.0
	for diameter_pair in diameters:
		print(math.sqrt(diameter_pair[1]))
		diameter_sum += math.sqrt(diameter_pair[1])

	print(diameter_sum / float(k))