import sys
import dendropy
from dendropy.calculate import treecompare

tns = dendropy.TaxonNamespace()
ref = dendropy.TreeList.get(path = sys.argv[1], schema='newick', taxon_namespace=tns)
est = dendropy.TreeList.get(path = sys.argv[2], schema='newick', taxon_namespace=tns)

tree_num = 0
for t in est:
	tree1 = t
	tree2 = ref[tree_num]
	tree1.encode_bipartitions()
	tree2.encode_bipartitions()
	print(treecompare.symmetric_difference(tree1, tree2))
	tree_num +=1