import os
import sys
import getopt 
import subprocess
import yaml 
import time


def run_command(data: dict):
    nodes = data['nodes']
    parameters = data['parameters']

    servers = []
    clients = []
    custom_tests = []
    basic_tests = []
    try:
        start = time.time()
        for x in data['nodes']['servers']:
            print(x, type(x))
            servers.append(x)
        print(servers, type(servers))
        for x in data['nodes']['clients']:
            clients.append(x)
        print(clients, type(clients))
        namespace = data['parameters']['namespace']
        print(namespace)
        for x in data['parameters']['basic-tests']:
            basic_tests.append(x) 
        print(basic_tests)
        for x in data['parameters']['custom-test']:
            custom_tests.append(x)
        print(custom_tests)
        optional = data['parameters']['optional']  # TODO
        optional = ' '.join(optional)
        print(optional)
        output_folder = data['parameters']['output-folder']
        print(output_folder)
        stop = time.time()
        print(stop - start)
    except KeyError:
        print('One of the keys does not exits. Check the selected yaml file.\n')
    
    # Test names as combination <server>-<client>-<customtest>.knbtest'
    for server in servers:
        for client in clients:
            for basic_test in basic_tests:
                if len(custom_tests):
                    for custom in custom_tests:
                        filename = '{svr}_{clt}.knbdata'.format(svr=server, clt=client)
                        command = ' '.join(['./knb', '-sn', server, '-cn', client, '-n', namespace, '-ot', basic_test, 
                        '-o data','-ccmd "', custom, '"', optional, '-f', filename ])
                        print(command)

                    #subprocess.run(['./knb', '-sn', server, '-cn', client, 
                     #               '-n', namespace, '-ot', basic_tests, '-o data',
                      #              '-ccmd "', custom, '"', optional, 
                       #             '-f', './%s/%s'%(output_folder, filename) ], capture_output=True)
                else:
                    filename = "%s-%s.knbdata"%(server, client)
                     #subprocess.run(['./knb', '-sn', server, '-cn', client, 
                    #               '-n', namespace, '-ot', basic_tests, '-o data',
                    #              optional,  
                    #             '-f', './%o/%f'%(output_folder, filename) ], capture_output=True)
          


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
