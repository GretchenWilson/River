from ete3 import Tree, faces, AttrFace, TreeStyle, NodeStyle
import argparse

class TreeVisualize(object):

    def __init__(self, tree, outgrouplist):
        self.tree = tree
        self.outgrouplist = outgrouplist
        self.clades = {}
        self.cladestats = {}

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


    def labelClades(self):
        
        colors = [NodeStyle(bgcolor="Red"), NodeStyle(bgcolor="DarkOrange"), NodeStyle(bgcolor="Yellow"), NodeStyle(bgcolor="Green")]
        count=-1
        for key, value in self.clades.items():
            count +=1
            dist = self.cladestats[key]
            
            MRCA = self.tree.get_common_ancestor(value)
            print "Clade: ", key, "\n\tClade Support: ", MRCA.support, "\n\tMax SNP Distance: ", dist, "\n\tIsolates: ", ", ".join(value)
            MRCA.name = key
            if dist == 0: 
                MRCA.set_style(colors[0])
            elif dist <= 5:
                MRCA.set_style(colors[1])
            elif dist <= 10:
                MRCA.set_style(colors[2])
            elif dist <= 15:
                MRCA.set_style(colors[3])
        return
    def find5SNPClades(self):
        
        return
    def layout(self, node):
        print node.name
        if node and not node.is_leaf():
            N = AttrFace("name", fsize=30)
            faces.add_face_to_node(N, node, 0, position ="aligned")
        
    def collectTreeStats(self, statfile):
        #Reads clade stat file and adds all stats to clade stat dict
        with open(statfile, 'r') as sfh:
            sfh.readline()
            for line in sfh:
                stats = line.strip().split()
                try:
                    self.cladestats[stats[0]].update({stats[1]: stats[2:len(stats)]})
                except KeyError:
                    self.cladestats[stats[0]] = {}
                    self.cladestats[stats[0]].update({stats[1]: stats[2:len(stats)]})
      
      #          if stats[0] == stats[1]:
       #             self.cladestats[stats[0]] = int(stats[4])
        print self.cladestats
        return
            
    def setcladelabels(self, labelfile):
        # Accepts a clade label file and converts to internal dictionary
        with open(labelfile) as lfh:
            lfh.readline()
            for line in lfh:
                line = line.strip().split(': ')
                self.clades[line[0]] = line[1].split(', ')
        #self.cladestats = {k:{} for k in self.clades.keys()}
        return self.clades

    def addoutgrouplabel(self, clades, labelcontent):
        self.clades['outgroup'] = labelcontent
        
        return self.clades
                                    
#if __name__ == "__main__":
#    parser = argparse.ArgumentParser(description= "DCLS Tree Visualization")
#    subparsers = parser.add_subparser
    
t2 = Tree("../SE_Javiana_102317/results/tree.dnd")
labels = "../SE_Javiana_102317/lyveset/msa/out.labels.tsv"
stats = "../SE_Javiana_102317/results/cladestats.tsv"
outgroup = ['PNUSAS006625', 'PNUSAS006632']
v = TreeVisualize(t2, outgroup)
v.setcladelabels(labels)
v.rootAtOutgroup()
v.collectTreeStats(stats)
#v.labelClades()
ts = TreeStyle()
ts.show_leaf_name = True
ts.show_branch_support = True
#ts.layout_fn = layout
#tf = ProfileFace()
print t2.write(format=1)
t2.ladderize()
t2.show(tree_style=ts)
