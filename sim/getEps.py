import os, math

ffile = open('dielectric_not_normalized_May12.txt', 'w')
counter = 0

density = {}
lines = open('step_num.txt', 'r').readlines()
for line in lines:
	line = line.strip().split()
	id = int(line[0])
	rho = float(line[-1])
	density[id] = rho

for i in range(1, 7153, 1):

	if os.path.isfile('%d/out' %i):
		lines = open('%d/out' %i, 'r').readlines()
		if len(lines) < 5:
			continue

		#print(lines)
		lines = lines[4].strip().split(':')[1].split(',')
		eps = float(lines[0])
		std = float(lines[1].split('=')[1])
		if not math.isnan(eps):
			ffile.write('%5d	%12.6f		%12.6f\n' %(i, eps, std))
			counter += 1
			print('----------- %05d-------------' %counter)


