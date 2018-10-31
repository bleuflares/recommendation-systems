import sys

if __name__ == "__main__":
	input_file = open(sys.argv[1], 'r')

	lines = []
	for line in input_file:
		lines.append(line)
	print(len(lines))
	for j in range(18):
		output_file = open("train_%d.txt" %j, 'w')
		for i in range(len(lines)):
			if 5000 * j > i or i >= 5000 * (j + 1):
				output_file.write(lines[i])
		output_file.close()
		

