#!/home/wilsonge/miniconda2/bin/python
import argparse

def run(args):
    print "Mashing to Reference Database"
    print "Directory:", args.directory
    print "Output:", args.output

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='river mash2ref [options] <directory> <output>', description='Compares a directory of MASH sketches to the MASH NCBI RefSeq database.')
    parser.add_argument('directory', help='Directory of sketches')
    parser.add_argument('output', help='Output directory prefix')
    parser.set_default(func=run)
    results = parser.parse_args()
    directory = results.directory
    output = results.output

