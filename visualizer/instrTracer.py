
def getAlgorithmFlow(filename,flow_filename):

	file = open(flow_filename)
	lines = file.readlines()

	flow = []

	for line in lines:
		if filename in line:
			flow.append(int(line.split('(')[1].split(')')[0]))
			
	return flow

if __name__ == "__main__":
	filename = 'quicksort.py'
	flow_filename = 'flow.txt'
	print getAlgorithmFlow(filename, flow_filename)
