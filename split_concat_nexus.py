from Bio.Nexus import Nexus
from Bio import AlignIO
import os,sys,glob,re

st_mb_block = 'begin mrbayes;\n\
set nowarn=yes autoclose=yes;\n\
charset Gene_12 = 4001-5000;\n\
charset Gene_10 = 2001-3000;\n\
charset Gene_19 = 11001-12000;\n\
charset Gene_17 = 9001-10000;\n\
charset Gene_15 = 7001-8000;\n\
charset Gene_16 = 8001-9000;\n\
charset Gene_11 = 3001-4000;\n\
charset Gene_14 = 6001-7000;\n\
charset Gene_7 = 17001-18000;\n\
charset Gene_8 = 18001-19000;\n\
charset Gene_5 = 15001-16000;\n\
charset Gene_9 = 19001-20000;\n\
charset Gene_0 = 1-1000;\n\
charset Gene_2 = 12001-13000;\n\
charset Gene_13 = 5001-6000;\n\
charset Gene_18 = 10001-11000;\n\
charset Gene_1 = 1001-2000;\n\
charset Gene_3 = 13001-14000;\n\
charset Gene_4 = 14001-15000;\n\
charset Gene_6 = 16001-17000;\n\
partition combined = 20: Gene_0, Gene_1, Gene_10, Gene_11, Gene_12, Gene_13, Gene_14, Gene_15, Gene_16, Gene_17, Gene_18, Gene_19, Gene_2, Gene_3, Gene_4, Gene_5, Gene_6, Gene_7, Gene_8, Gene_9;\n\
set partition=combined;\n\
speciespartition species = Sp1: t1 t2 t3, Sp2: t4 t5 t6, Sp3: t7 t8 t9, Sp4: t10 t11 t12, Sp5: t13 t14 t15, Sp6: t16 t17 t18, Sp7: t19 t20 t21, Sp8: t22 t23 t24;\n\
set speciespartition = species;\n\
unlink topology=(all);\n\
prset topologypr = speciestree;\n\
prset brlenspr = clock:speciestree;\n\
lset nst=2 rates=gamma;\n\
prset popvarpr=equal;\n\
prset popsizepr = normal(0.0025, 0.1);\n\
prset Statefreqpr = fixed(empirical);\n\
prset Shapepr = fixed(0.8);\n\
prset tratiopr = fixed(3);\n\
mcmc ngen=30000000 nchains=4 nruns=4 stoprule=yes;\n\
sumt contype=allcompat;\n\
end;'

concat_mb_block = 'begin mrbayes;\n\
set nowarn=yes autoclose=yes;\n\
lset nst=2 rates=gamma;\n\
prset Statefreqpr = fixed(empirical);\n\
prset Shapepr = fixed(0.8);\n\
prset tratiopr = fixed(3);\n\
mcmc ngen=30000000 nchains=4 nruns=4 stoprule=yes;\n\
sumt contype=allcompat;\n\
end;'

def split_file(file,DIR):
	with open(file) as f:
		lines = f.readlines()[18:]
		counter = 0
		for line in lines:
			if line.startswith('Begin'):
				outfile = open(DIR+'Gene_'+str(counter)+'.nexus', 'w')
				outfile.write('#NEXUS\n\n')
				outfile.write(line)
			elif line.startswith('END'):
				outfile = open(DIR+'Gene_'+str(counter)+'.nexus', 'a')
				outfile.write(line)
				counter += 1
			else:
				outfile = open(DIR+'Gene_'+str(counter)+'.nexus', 'a')
				outfile.write(line)


if __name__ == "__main__":
	DIR = sys.argv[1]
	if DIR[-1] != "/": DIR += "/"
	for nex in glob.glob(DIR+'*_Seq'):
		file_list = []
		split_file(nex,DIR)
		for file in glob.glob(DIR+'*.nexus'):
			file_list.append(file)
		nexi = [(fname, Nexus.Nexus(fname)) for fname in file_list]
		combined = Nexus.combine(nexi)
		st_nex = open(nex+'.speciestree.nex', 'w')
		concat_nex = open(nex+'.concat.nex', 'w')
		combined.write_nexus_data(filename=st_nex,interleave=True)
		st_nex.write(st_mb_block)
		combined.write_nexus_data(filename=concat_nex,interleave=True)
		concat_nex.write(concat_mb_block)
		for file in glob.glob(DIR+'*.nexus'):
			os.remove(file)
		
