import sys, os

with open(sys.argv[1], 'r') as read_file:
	for line in read_file.readlines():
		line = line.strip().split()[0]
		os.system('cp SingleNodeXYZ/Stack_%d.xyz Br/SingleNodeXYZ/.' %int(line))

		os.system('mkdir Br/RUNS/%d' %int(line))
		os.system('mkdir Br/RUNS/%d/init' %int(line))	
		os.system('mkdir Br/RUNS/%d/DAT' %int(line))
		os.system('mkdir Br/RUNS/%d/src' %int(line))

		os.system('cp Br/SingleNodeXYZ/Stack_%d.xyz Br/RUNS/%d/init/.' %(int(line), int(line)))
		os.system('cp RXMD-Test/theta/2/rxmd Br/RUNS/%d/.' %int(line))
		os.system('cp RXMD-Test/theta/2/init/geninit Br/RUNS/%d/init/.' %int(line))
		os.system('cp RXMD-Test/theta/2/ffield Br/RUNS/%d/.' %int(line))
		os.system('cp RXMD-Test/theta/2/rxmd.in* Br/RUNS/%d/.' %int(line))

		os.system('cd Br/RUNS/%d/init; ./geninit -i Stack_%d.xyz -n; cd ../../../../' %(int(line), int(line)))
		os.system('cd Br/RUNS/%d/init; ./geninit -i norm.xyz; cd ../../../../' %(int(line)))
		os.system('cp Br/RUNS/%d/init/rxff.bin Br/RUNS/%d/DAT/.' %(int(line), int(line)))

		print('%06d' %int(line))	
