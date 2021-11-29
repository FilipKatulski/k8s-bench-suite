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

To see the full description of parameters required by knb script please use "-k" flag.

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
                    #f = open(logname, 'w')
                    subprocess.call(command, shell=True)
            else:
                filepath = './{folder}/{svr}_{clt}.knbdata'.format(folder=output_folder, svr=server, clt=client)
                command = ' '.join(['./knb', '-sn', server, '-cn', client, '-n', namespace, '-ot', basic_tests, 
                '-o data', optional, '-f', filepath])
                logname = './{folder}/{svr}_{clt}.txt'.format(folder=output_folder, svr=server, clt=client)
                #f = open(logname, 'w')
                subprocess.call(command, shell=True)


# TODO 
def plot_data(inputconfig: dict):
    """
    This function provides 
    :param inputfolder: String with inputfolder name to generate png files from.
    """
    input_folder = ''
    output_folder = ''
    namespace = ''
    optional = ''
    kubecfg = ''

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
            output_folder = output_folder + '/' + filename
            output_folder = output_folder[:-8]
            print(output_folder)
            input_dir = input_folder + '/' + filename
            print(input_dir)
            command = ' '.join(['./knb', '-n', namespace, '-fd', input_dir, '--plot', '--plot-dir', output_folder, optional])
            print(command)
            subprocess.call(command, shell=True)
            exit()
        else:
            continue
    


def main (argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv, "khi:pd:",["knb-help","help", "input-file", "plotting-mode", "plot-dir"])
    except getopt.GetoptError:
        sys.exit("Autotester failed to parse optipns.\n")
    for opt, arg in opts:
        if opt in ('-k', '--knb-help'):
            display_knb_help()
            sys.exit()
        elif opt in ('-h', '--help'):
            display_help()
            sys.exit()
        elif opt in ('-i', '--input-file'):
            inputfile = arg 
            print('Input file is "',inputfile, '"\n')
            test_data = parse_yaml(inputfile)
            run_tests(test_data)
        else:
            assert False, "unhandled option"

def argument_parser():
    """
    This function parses the arguments provided for the script.
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
    parser.add_argument('-kubecfg', '--kube-config', dest='kubecfg', required=False, 
    help='Speficied kubeconfig file used for plotting')

    args = parser.parse_args()
    
    print(args)
    if args.help:
        display_help()
    if args.knb_help:
        display_knb_help()
    if args.input:
        if args.plot:
            print('lel')
            plot_config = parse_yaml(args.input)
            plot_data(plot_config)
        else:
            print('lol')
            test_data = parse_yaml(args.input)
            #run_tests(test_data)
    


if __name__ == "__main__":
    argument_parser()
    #main(sys.argv[1:])
