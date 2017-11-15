from ete3 import Tree, faces, AttrFace, TreeStyle, NodeStyle
import argparse

class TreeVisualize(object):

    def __init__(self, tree, outgrouplist):
        self.tree = tree
        self.outgrouplist = outgrouplist
        self.clades = None
        self.cladestats = None
        self.signif_clades = []
        
    def rootAtOutgroup(self):
        rootnode = None
        if len(self.outgrouplist) > 1:
            rootnode = self.tree.get_common_ancestor(self.outgrouplist)
        else:
            rootnode = self.outgrouplist[0]
        try:
            self.tree.set_outgroup(rootnode)
        except Exception:
            print "Outgroups do not have an MRCA"
        return self.tree

    def defineClades(self, labelfile):
        # Accepts a clade label file and converts it into a clade-isolate dictionary
        self.clades = {}
        with open(labelfile) as lfh:
            lfh.readline()
            for line in lfh:
                line = line.strip().split(': ')
                self.clades[line[0]] = line[1].split(', ')
        return
    
    def collectStats(self, statfile):
        # Reads clade stat file and adds all stats to clade stat dict
        self.cladestats = {}
        with open(statfile, 'r') as sfh:
            sfh.readline()
            for line in sfh:
                if line.startswith("Tree"):
                    continue
                stats = line.strip().split()
                try:
                    self.cladestats[stats[0]].update({stats[1]:
                                                      [int(k) for k in stats[2:len(stats)]]})
                except KeyError:
                    self.cladestats[stats[0]] = {}
                    self.cladestats[stats[0]].update({stats[1]:
                                                      [int(k) for k in stats[2:len(stats)]]})
        return

    def labelClades(self):
        # Label tree nodes according to data specified in the collectStats and defineClades functions
        if not self.clades:
            print "Must define clades prior to labelling. \nSubmit Lyve-SET CladeLabel file"
            exit
        if not self.cladestats:
            print "Must provide clade stats prior to labelling. \nSubmit Lyve-SET CladeStats file"    
            exit
        for key,value in self.cladestats.items():
            print key
            node = key
            if key in self.clades.keys():
                node = self.tree.get_common_ancestor(self.clades[key])
                node.name = key
                stats = self.cladestats[node.name]["Rest"]
                
            else:
                node = self.tree.search_nodes(name=key)[0]
                #node = self.tree&key
            node.add_features(snp_min=stats[1], snp_max=stats[2], snp_MAD=stats[3])
            #for key, value in self.clades.items():
            #MRCA = self.tree.get_common_ancestor(value)
            #MRCA.name = key
            #try:
             #   stats = self.cladestats[MRCA.name]["Rest"]
             #   MRCA.add_features(snp_min=stats[1], snp_max=stats[2], snp_MAD=stats[3])
             #   print "Clade: ", key, "\n\tClade Support: ", MRCA.support, "\n\tMinimum SNPs to Neighbor: ", MRCA.snp_min, "\n\tIsolates: ", ", ".join(value)
            #except KeyError:
             #   print "MRCA ", MRCA.name, " was not identified in the Clade Stats File"          

        return

    def labelSignificance(self):
        print self.cladestats.keys()
        root = self.tree.get_tree_root()
        print root
        root.name = "Root"
        self.searchNode(root)
        return

    def searchNode(self, node):
        if not node.is_leaf():
            print "Internal Node: ", node.name
            if len(node.get_children()) > 2:
                node.resolve_polytomy(recursive=False)
                
            children = node.get_children()
            print "\tChildren: ", children
            try:
                if children[0].name in self.cladestats.keys() and children[0].snp_min <= 10 or children[1].name in self.cladestats.keys() and children[0].snp_min <= 10:
                    node.set_style(NodeStyle(bgcolor="Red"))
                    print "Significant Clade: ", node.name
                    return
            except Exception:
                print 
            self.searchNode(children[0])
            self.searchNode(children[1])
            return
        else:
            print "Leaf: ", node.name
            return
                
    #if __name__ == "__main__":
#    parser = argparse.ArgumentParser(description= "DCLS Tree Visualization")
#    subparsers = parser.add_subparser
    
t2 = Tree("../SE_Javiana_102317/results/tree.dnd")
labels = "../SE_Javiana_102317/lyveset/msa/out.labels.tsv"
stats = "../SE_Javiana_102317/results/cladestats.tsv"
outgroup = ['PNUSAS006625', 'PNUSAS006632']
v = TreeVisualize(t2, outgroup)
v.rootAtOutgroup()
v.defineClades(labels)
v.collectStats(stats)
v.labelClades()
v.labelSignificance()
ts = TreeStyle()
ts.show_leaf_name = True
ts.show_branch_support = True
#ts.layout_fn = layout
#tf = ProfileFace()
#print t2.write(format=1)
t2.ladderize()
t2.show(tree_style=ts)
