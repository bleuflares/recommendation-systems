import sys
import numpy as np
from pyspark import SparkConf, SparkContext

def distance(arr1, arr2):
	dist = 0
	for i in range(len(arr1)):
		dist += (arr1[i] - arr2[i]) * (arr1[i] - arr2[i])
	return (dist)

if __name__ == "__main__":
	input_file = open(sys.argv[1], 'r')
	k = sys.argv[2]

	points = []
	k_means = []
	k_means_indices = []

	for line in input_file:
		point = line.split()
		points.append(point)

	distances = np.zeros((len(points), len(points)))

	for i in range(len(points)):
		for j in range(len(points)):
			distances[i, j] = distance(points[i], point[j])
	x, y = np.unravel_index(distances.argmax(), distances.shape)
	k_means.append(points[x])
	k_means.append(points[y])
	k_means_indices.append(x)
	k_means_indices.append(y)
	k_means_exclude = list(set(range(len(points))) - set(k_means_indices))

	while len(k_means) < k:
		row_idx = np.array(k_means_indices)
		col_idx = np.array(k_means_exclude)
		a = distances[row_idx[:, None], col_idx]
		x, y = np.unravel_index(a.argmax(), a.shape)
		k_means.append(points[y])
		k_means_indices.append(y)
		k_means_exclude = list(set(range(len(points))) - set(k_means_indices))
	print(k_means_exclude)

	def k_means_distance(arr):
		min_dist = 0
		min_point = None
		for point in k_means:
			dist = 0
			for i in range(len(arr)):
				dist += (point[i] - arr[i]) * (point[i] - arr[i])
			if dist < min_dist:
				min_dist = dist
				min_point = point
		return (point.index(min_point), min_dist)

    conf = SparkConf()
    sc = SparkContext(conf=conf)
    lines = sc.textFile(sys.argv[1])
    points = lines.flatmap(lambda ids: ids.split())
    centroids_map = points.map(lambda p: k_means_distance(p))
    print(centroids_map.reduceByKey(lambda a, b: a + b).collect())

