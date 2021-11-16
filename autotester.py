import os
import sys
import getopt 
import subprocess
import yaml 


def run_command(data: dict):
    for key, value in data.items():
        print(key, ' : ', value)
    ...

def parse_yaml(filepath: str) -> dict:
    with open(filepath, "r") as stream:
        try:
            data = yaml.safe_load(stream)
            print(data)
            print(type(data))
        except yaml.YAMLError as yerr:
            print(yerr)
    return data


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
            inputfile = arg 
    
    print('Input file is "',inputfile, '"')
    test_data = parse_yaml(inputfile)
    run_command(test_data)


if __name__ == "__main__":
    main(sys.argv[1:])
