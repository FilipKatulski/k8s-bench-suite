import os
import sys
import getopt 
import subprocess
import yaml
import argparse
from typing import Optional
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


def display_help(): 
    """
    Displays the full help message for this script usage.
    """
    display_header()
    print('''knb is a network benchmark tool for Kubernetes CNI.
Autotester script is used to automate running multiple knb tests one by one or create plots for multiple tests,
according to provided yaml files.
The output testing data is saved to a tar file. Test names as combination '<server>-<client>-<customtestindex>.knbtest'.
The output plots are png files saved in the directory named after the test, at the specified location.

==========
PARAMETERS
==========

    -h, --help              |

    -k, --knb-help          |



=======
TESTING
=======

Required parameters are:
- server and client nodes
- namespace
- output-folder

Optional parameters:
- basic-tests
- custom-tests
- optional
- kubeconfig-file

To see the full description of parameters required by knb script please use "-k" flag.

Input test specification yaml file should follow this structure:
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

========
PLOTTING
========

Required parameters are:
- input-folder
- output-folder
- namespace

Optional parameters are:
- kubeconfig-file
- optional

To see the full description of parameters required by knb script please use "-k" flag.

Input plotting specification yaml file should follow this structire:
_________________________________________________
parameters:
  input-folder:
    testing101
  namespace:
    knbtest
  optional:
    - -v
    - --debug
  output-folder:
    "./testing101/plots"
  kubeconfig-file:
    "/afs/cern.ch/user/f/fkatulsk/private/FKatulskiOpenStack.conf"

_________________________________________________

    ''')


def display_knb_help():
    """
    Displays knb shell script helper.
    """
    display_header()
    subprocess.call(['./knb', '-h'], shell=True)


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


def run_tests(data: dict):
    """
    Runs tests specified in the yaml file, according to description.
    :param data: dictionary with parsed parameters for tests.
    """

    display_header()

    servers = []
    clients = []
    pairs = []
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
        
        #TODO change to 'pairs' instead of 'servers' and 'clients' 
        if 'pairs' in data['nodes'].keys():
            print(data['nodes']['pairs'], type(data['nodes']['pairs']))
            pairs = data['nodes']['pairs']
            for pair in pairs:
                
                pair = tuple(pair.split(', '))
                print(pair, type(pair))
                print(pair[0], type(pair[0]))
                servers.append(pair[0])
                clients.append(pair[1])

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
                    #f = open(logname, 'w')
                    #subprocess.call(command, shell=True)
            else:
                filepath = './{folder}/{svr}_{clt}.knbdata'.format(folder=output_folder, svr=server, clt=client)
                command = ' '.join(['./knb', '-sn', server, '-cn', client, '-n', namespace, '-ot', basic_tests, 
                '-o data', optional, '-f', filepath])
                logname = './{folder}/{svr}_{clt}.txt'.format(folder=output_folder, svr=server, clt=client)
                #f = open(logname, 'w')
                #subprocess.call(command, shell=True)


def plot_data(inputconfig: dict):
    """
    This function provides 
    :param inputfolder: Dictionary with parameters for plotting
    """
    input_folder = ''
    output_folder = ''
    namespace = ''
    optional = ''
    kubeconfig = ''

    try:
        input_folder = inputconfig['parameters']['input-folder']
        print(inputconfig['parameters']['input-folder'], type(inputconfig['parameters']['input-folder']))
        output_folder += inputconfig['parameters']['output-folder']
        print(inputconfig['parameters']['output-folder'], type(inputconfig['parameters']['output-folder']))
        namespace = inputconfig['parameters']['namespace']
        print(namespace)

        if 'optional' in inputconfig['parameters'].keys():
            optional = inputconfig['parameters']['optional']
            optional = ' '.join(optional)

        if 'kubeconfig-file' in inputconfig['parameters'].keys():
            kubeconfig_file = inputconfig['parameters']['kubeconfig-file']
            kubeconfig = ' -kubecfg ' + kubeconfig_file
            optional = optional + kubeconfig

    except KeyError:
        exit('One of the required keys does not exist.\nCheck the selected yaml and list of required parameters.\n')
    
    for filename in os.listdir(input_folder):
        if filename.endswith('.knbdata'):
            print(filename, type(filename))
            output = output_folder + '/' + filename
            # Deletes '.knbdata' suffix:
            output = output[:-8]
            input_dir = input_folder + '/' + filename
            
            if not os.path.exists(output):
                os.makedirs(output)

            command = ' '.join(['./knb', '-n', namespace, '-fd', input_dir, '--plot', '--plot-dir', output, optional])
            print(command)
            subprocess.call(command, shell=True)
        else:
            continue


def main():
    """
    The main function parses arguments provided for the script and runs specified functions.
    """
    def _is_valid_file(parser, arg):
        if not os.path.exists(arg):
            parser.error("The specified file does not exist.\n")
        else:
            return arg

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-h', '--help', action='store_true', help="displays autotester script help")
    parser.add_argument('-k','--knb-help', action='store_true', help='displays knb script help')
    parser.add_argument('-i', '--input', dest='input', required=False, metavar='FILE', 
    type=lambda x: _is_valid_file(parser, x), 
    help='input yaml file with test configuration or input folder for plotting')
    parser.add_argument('-p', '--plot', action='store_true', help='create plots from selected folder')

    args = parser.parse_args()
    
    if args.help:
        display_help()
    if args.knb_help:
        display_knb_help()
    if args.input:
        if args.plot:
            plot_config = parse_yaml(args.input)
            plot_data(plot_config)
        else:
            test_config = parse_yaml(args.input)
            run_tests(test_config)
    

if __name__ == "__main__":
    main()
