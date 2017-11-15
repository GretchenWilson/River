#!/home/wilsonge/miniconda2/bin/python
import actions, argparse, subprocess
from glob import glob
from os import makedirs, mkdir, path, getcwd, chdir, symlink, listdir, walk

def run(args):

    project = args.project_name
    reference = path.abspath(args.reference)
    directory = args.directory if args.directory else args.BS_project
    output = path.abspath(args.output)
    
    project_dir = path.join(output, project)
    interleaved = path.join(output, project, 'interleaved_files')
    reads = path.join(project_dir, 'raw_reads')
    starting_directory = getcwd()
    
    print "Project:", project
    print "Reference:", reference
    print "Reads Directory:", directory
    print "Output Directory:", output

    try:    
        makedirs(interleaved)
        mkdir(reads)

    except Exception:
        print "\nError:: Project name exists in output directory. Please provide a unique project name.\n" 
        exit(0)

        
    #link reads
    for dir,_,_ in walk(directory):
        for read_file in glob(path.join(dir, '*.fastq*')):
            symlink(read_file, path.join(reads, path.basename(read_file)))
        
    #interleave 1 and 2 read files and place into interleaved_files directory
    chdir(reads)
    subprocess.call('shuffleSplitReads.pl *.fastq* --numcpus 4 -o ' + interleaved, shell=True )
        
    #create lyveset directory structure and add symlinks to reads and reference
    chdir(project_dir)
    subprocess.call(['set_manage.pl', '--create', 'lyveset'])
    lyveset_dir = path.join(project_dir, 'lyveset')
    lyveset_reference = path.join(lyveset_dir ,'reference', path.basename(reference))
    symlink(reference, lyveset_reference)
    for fastq in listdir(interleaved):
        symlink(path.join(interleaved, fastq), path.join(lyveset_dir, 'reads', fastq))
    call_set = ['launch_set.pl', lyveset_dir, '-ref', lyveset_reference, '--presets', 'salmonella_enterica', '--numcpus', '3']
    print " ".join(call_set)
    subprocess.call(call_set)
    finish(project_dir)

def finish(project_path):
    results = path.join(project_path, 'results')
    mkdir(results)
    lyveset = path.join(project_path, 'lyveset', 'msa')
    symlink(path.join(lyveset, 'out.RAxML_bipartitions'), path.join(results, 'tree.dnd'))
    symlink(path.join(lyveset, 'out.labels.tsv'), path.join(results, 'labels.tsv'))
    symlink(path.join(lyveset, 'out.merged.cladestats.tsv'), path.join(results, 'cladestats.tsv'))
    symlink(path.join(lyveset, 'out.pairwiseMatrix.tsv'), path.join(results, 'pairwiseMatrix.tsv'))
    


            
            
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser('DCLS lyveset script',
                                      usage='lyveset.py <project_name> <read_directory> <reference> [options]',
                                      description='Creates directory structure and runs lyveset snp profiling and phylogeny')
    parser.add_argument('project_name', help='Unique name for project run')
    parser.add_argument('directory', action=actions.DirectoryExists, help='Directory location of reads')
    parser.add_argument('reference', action=actions.FileExists, help='Path to reference sequence')
    parser.add_argument('-o', action=actions.DirectoryExists, dest='output', default='./', help='Directory to build lyveset. default = current directory')
    parser.set_defaults(func=run)

    #Parse command
    #pass arguments to the function defined by the specified subcommand
    arguments = parser.parse_args()
    arguments.func(arguments)
