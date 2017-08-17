from Bio import Phylo
import os,sys,glob,re
import copy

DIR = sys.argv[1]
if DIR[-1] != "/": DIR += "/"

t_list = ['t2','t3','t5','t6','t8','t9','t11','t12','t14','t15','t17','t18','t20','t21','t23','t24']

for t in os.listdir(DIR):
	if t.endswith('nex.con.tre.new'):
		name = t.split('.')[0]
		tree = Phylo.read(DIR+t, "newick")
		newtree = copy.deepcopy(tree)
		for p in t_list:
			newtree.prune(p)
		Phylo.write(newtree, DIR+name+".concat.trimmed.tre", "newick")	