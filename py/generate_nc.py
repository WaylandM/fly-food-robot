#!/usr/bin/env python

# limit numboxes input to one or two
# check for presence of file directory and prompt user to confirm overwrite

# list configuration in comments at top of gcode file

VERSION = "0.0.1"

import argparse

def(generateNC):
    
    


if __name__ == "__main__":
    """ Parse the command line arguments """
    parser = argparse.ArgumentParser(description='Align RNA-seq reads.')
    parser.add_argument('idx', nargs=1, help='tar archive containing genome index files')
    parser.add_argument('fastq', metavar='FASTQ', nargs='+', help='names and paths of fastq files')
    parser.add_argument('--numcpus', type=int, metavar='NUMCPU', nargs=1, help='Number of CPUs available', default=[1])
    parser.add_argument("--version", action='version', version=VERSION) 
    args = parser.parse_args()

    """ Run the desired methods """
    generateNC(args)





# filename (mandatory)
# filltime (-t)
# pause (-p drip pause default 0.1)
# numboxes (-b)
# numrows (-r)
# numcolumns (-c)
# x1
# y1
# x2
# y2
# x3
# y3
# x4
# y4
# zclearance (-z)
# --no-homing (don't home before running job) boolean
# comments (add comment to top of file)
# version (--version)



