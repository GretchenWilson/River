import argparse
from os.path import isdir, isfile, join, expanduser

class DirectoryExists(argparse.Action):
    def __call__(self, parser, namespace, values, options_string=None):
        if not isdir(values):
            print "Directory", values
            raise ValueError("Directory " + values + " does not exist!")
        setattr(namespace, self.dest, values)
        return

class BaseSpaceDirectory(argparse.Action):
    def __call__(self, parser, namespace, values, options_string=None):
        
        values = join(expanduser('~'),'BaseSpace/Projects', values, 'Samples')
        if not isdir(values):
            raise ValueError("BaseSpace project "+ values + " does not exist. \nPlease check Project id and make sure BaseSpace is properly mounted in your home directory. \n $ basemount ~/BaseSpace")
        setattr(namespace, self.dest, values)
        return
            
class FileExists(argparse.Action):
    def __call__(self, parser, namespace, values, options_string=None):
        if not isfile(values):
            print "Reference", values
            raise ValueError("Reference does not exist!")
        setattr(namespace, self.dest, values)
        return
