import sys

if __name__ == "__main__":
	input_file = open(sys.argv[1], 'r')

	lines = []
	for line in input_file:
		lines.append(line)
	print(len(lines))
	for j in range(18):
		output_file = open("test_%d.txt" %j, 'w')
		for i in range(5000):
			if 5000 * j + i >= len(lines):
				break
			output_file.write(lines[5000 * j + i])
		output_file.close()
		

