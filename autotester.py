import os
import sys
import getopt 
import subprocess
import json
import yaml


def run_command():
    ...

def parse_yaml():
    ...


def main (argv):
    inputfile = ''

    try:
        opts, args = getopt.getopt(argv, "hi:",["help", "input-file"])
    except getopt.GetoptError:
        print('autotester.py failed to parse arguments.\n')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("TODO help here")
            sys.exit()
        elif opt in ('-i', '--input-file'):
            

if __main__ == "__main__":
    main(sys.argv[1:])
