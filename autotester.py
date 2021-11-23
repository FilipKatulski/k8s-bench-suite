import os
import sys
import getopt 
import subprocess
import yaml
from time import sleep 
try:
    from art import text2art
except ModuleNotFoundError:
    print("\n\n'Art' module is not installed\n")
    pass

def display_header():
    """
    Displays python art header.
    """
    try:
        art_1 = text2art("knb autotester")
        print(art_1)
        sleep(1)
    except:
        print("\nknb autotester\n\n")
        sleep(1)


def display_help():  # TODO 
    """
    Displays the full help message for this script usage.
    """
    display_header()
    print('''knb is a network benchmark tool for Kubernetes CNI.
Autotester script is used to automate running multiple knb tests one by one, according to provided yaml file.
The output data is saved to a tar file. Test names as combination '<server>-<client>-<customtestindex>.knbtest'.

Required parameters are:
- server and client nodes
- namespace
- output-folder

Optional parameters:
- basic-tests
- custom-tests
- optional
- kubeconfig-file

To see the full description of parameters required by knb script please use "./knb -h"

Input yaml file should follow this structure:
_________________________________________________
nodes:
  servers:
    - node-k8s-1
    - node-k8s-2
    - node-k8s-3
  clients:
    - node-k8s-2
    - node-k8s-4
    - node-k8s-6
parameters:
  namespace:
    knbtest
  basic-tests:
    - p2p
    - tcp
  custom-tests:
    - "--cport 5201 -O 1 -f m -t 10"
    - "--cport 5202 -O 1 -f m -t 20"
  optional:
    - -v
    - --debug
    - -hnc
    - -hns
  output-folder:
    testing101
  kubeconfig-file:
    "/path/to/kubeconfig/file"
_________________________________________________
    
    ''')


def run_tests(data: dict):
    """
    Runs tests specified in the yaml file, according to description.
    :param data: dict with parsed parameters for tests.
    """

    display_header()

    servers = []
    clients = []
    basic_tests = []
    custom_tests = []
    kubeconfig_file = ''
    output_folder = ''
    optional = ''
    
    try:
        # Required parameters:
        for x in data['nodes']['servers']:
            servers.append(x)
        for x in data['nodes']['clients']:
            clients.append(x)
        
        namespace = data['parameters']['namespace']

        output_folder = data['parameters']['output-folder']

        # Optional parameters:
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
        
        if 'optional' in data['parameters'].keys():
            optional = data['parameters']['optional']
            optional = ' '.join(optional)

        if 'kubeconfig-file' in data['parameters'].keys():
            kubeconfig_file = data['parameters']['kubeconfig-file']
            kubeconfig = ' -kubecfg ' + kubeconfig_file
            optional = optional + kubeconfig
        
    except KeyError:
        exit('One of the required keys does not exist.\nCheck the selected yaml and list of required parameters.\n')    

    # Test names as combination '<server>-<client>-<customtest>.knbtest'
    for server in servers:
        for client in clients:
            if custom_tests:
                for i, custom in enumerate(custom_tests):
                    filepath = './{folder}/{svr}_{clt}_custom{index}.knbdata'.format(folder=output_folder, 
                    svr=server, clt=client, index=i)
                    command = ' '.join(['./knb', '-sn', server, '-cn', client, '-n', namespace, '-ot', basic_tests,
                    '-o data','-ccmd "', custom, '"', optional, '-f', filepath ])
                    logname = './{folder}/{svr}_{clt}_custom{index}.txt'.format(folder=output_folder, svr=server, 
                    clt=client, index=i)
                    f = open(logname, 'w')
                    subprocess.call(command, shell=True, stdout=f)
            else:
                filepath = './{folder}/{svr}_{clt}.knbdata'.format(folder=output_folder, svr=server, clt=client)
                command = ' '.join(['./knb', '-sn', server, '-cn', client, '-n', namespace, '-ot', basic_tests, 
                '-o data', optional, '-f', filepath])
                logname = './{folder}/{svr}_{clt}.txt'.format(folder=output_folder, svr=server, clt=client)
                f = open(logname, 'w')
                subprocess.call(command, shell=True, stdout=f)


def parse_yaml(filepath: str) -> dict:
    """
    This function parses provided yaml file with PyYAML library. 
    :param filepath: String with filepath to specified yaml file with tests' description
    """
    with open(filepath, "r") as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as yerr:
            print(yerr)
            exit("Could not load the test file.\n")
    return data


def main (argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:",["help", "input-file"])
    except getopt.GetoptError:
        sys.exit("Autotester failed to parse arguments.\n")
    for opt, arg in opts:
        if opt == '-h':
            display_help()
            sys.exit()
        elif opt in ('-i', '--input-file'):
            inputfile = arg 
            print('Input file is "',inputfile, '"\n')
            test_data = parse_yaml(inputfile)
            run_tests(test_data)


if __name__ == "__main__":
    main(sys.argv[1:])
