import os
import sys
import getopt 
import subprocess
import yaml 
import time


def run_command(data: dict):
    servers = []
    clients = []
    basic_tests = []
    custom_tests = []
    output_folder = ''
    optional = ''

    try:
        start = time.time()
        for x in data['nodes']['servers']:
            servers.append(x)
        for x in data['nodes']['clients']:
            clients.append(x)
        namespace = data['parameters']['namespace']
        if 'basic-tests' in data['parameters'].keys():
            basic_tests = data['parameters']['basic-tests']
            basic_tests = ','.join(basic_tests)
        else: 
            basic_tests = 'all'
        if 'custom-tests' in data['parameters'].keys():
            for x in data['parameters']['custom-tests']:
                custom_tests.append(x)
        else:
            custom_tests = False 
        optional = data['parameters']['optional']
        optional = ' '.join(optional)
        output_folder = data['parameters']['output-folder']
        stop = time.time()
        print(stop - start)
    except KeyError:
        print('One of the keys does not exits. Check the selected yaml file.\n')
    
    # Test names as combination <server>-<client>-<customtest>.knbtest'
    for server in servers:
        for client in clients:
            if custom_tests:
                for i, custom in enumerate(custom_tests):
                    print(basic_tests, type(basic_tests))
                    filepath = './{folder}/{svr}_{clt}_custom{index}.knbdata'.format(folder=output_folder, 
                    svr=server, clt=client, index=i)
                    command = ' '.join(['./knb', '-sn', server, '-cn', client, '-n', namespace, '-ot', basic_tests,
                    '-o data','-ccmd "', custom, '"', optional, '-f', filepath ])
                    print('Command, <type>: ', command, type(command))
                    subprocess.call(command, shell=True)
            else:
                filepath = './{folder}/{svr}_{clt}.knbdata'.format(folder=output_folder, svr=server, clt=client)
                command = ' '.join(['./knb', '-sn', server, '-cn', client, '-n', namespace, '-ot', basic_tests, 
                '-o data', optional, '-f', filepath])
                print('Command, <type>: ',command, type(command))
                subprocess.call(command, shell=True)


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
