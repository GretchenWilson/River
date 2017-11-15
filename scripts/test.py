import os
from glob import glob

basespace = '/home/wilsonge/BaseSpace/Projects/Belvidere_Validation_E.coli/Samples/'
project = '/home/wilsonge/Datasets/Minnesota_Salmonella-enterica-Enteritidis'
filenames = []
for directory,_ ,_ in os.walk(project):
    filenames.extend(glob(os.path.join(directory, '*.fastq*')))

print "\n".join(filenames)
