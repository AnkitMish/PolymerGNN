import sys

steps = open('step_num.txt', 'w')
counter  = 0

steps.write("file_id   start_step   end_step   chain_length  lata   latb   latc   density \n")

br_ids = open('Br_ids.txt', 'r')
lines = br_ids.readlines()
br_ids = []
for line in lines:
	br_ids.append(int(line.strip().split()[0]))

chain_length = open('chain_length.txt', 'r')
lines = chain_length.readlines()
chain_length = {}
for line in lines:
	line = line.strip().split()
	step = int(line[0])
	natoms = int(line[1])
	chain_length[step] = natoms

for i in range(1, 7233):
	if i in br_ids:
		continue

	read_file = open('%d/out' %i, 'r')

	step = None
	dens = None
	md_step = None

	for line in read_file.readlines():
		line = line.strip().split(':')
		step = int(line[0])
		dens = float(line[-1])
		found = False
		lata, latb, latc = None, None, None

		if dens > 1.38:
			counter += 1
			steps_read = open('%d/compress%d' %(i,i),'r')
			lineNum = 0
			while True:
				try:
					line = steps_read.readline()
				except UnicodeDecodeError as e:
					print('Unable to read some part of %d/compress%d due to error: %s ' %(i,i, e))
					break

				if not line:
					break

				lineNum += 1

				if lineNum == step - 2:
					line = line.split(':')[1].split()
					lata, latb, latc = float(line[0]), float(line[1]), float(line[1])


				if lineNum == step:
					found = True
					line = None
					for j in range(11):
						try:
							line = steps_read.readline()
						except UnicodeDecodeError as e:
							print('Unable to read some part of %d/compress%d due to error: %s ' %(i,i, e))
							break

					if found:
						md_step = line.strip()
						md_step = md_step.split(':')
						md_step = md_step[1]
						md_step = md_step.split()
						md_step = int(md_step[0])
						break				
	
			if found:
				steps.write('%6d  %6d  %6d  %6d  %12.6f  %12.6f  %12.6f  %12.6f \n' %(i, md_step, md_step + 500, chain_length[i], lata, latb, latc, dens))

				print('%6d %6d %6d %12.6f ' %(i, counter, md_step, dens))

			break
