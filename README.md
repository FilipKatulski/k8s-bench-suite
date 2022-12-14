# k8s-bench-suite
Bash and Python scripts collection to benchmark Kubernetes cluster performance. Modified to meet ATLAS P1 Kubernetes cluster's demands by me, FilipKatulski, during my cooperation with EP-ADT-DQ group at ATLAS project, CERN.

The creator of the original version is Alexis Ducastel <alexis@infrabuilder.com>, which can be found [here](https://github.com/InfraBuilder/k8s-bench-suite).

## [knb](knb) : Kubernetes Network Benchmark

[knb](knb) is a bash script that will start a networking benchmark on a target Kubernetes cluster.

Here are some highlights:

- **Plain bash script** with very few dependencies
- Complete benchmark **takes only 2 minutes**
- Ability to select only a subset of benchmark tests to run
- Testing **both TCP and UDP** bandwidth
- **Automatic detection of CNI MTU**
- **Includes host cpu and ram monitoring** in benchmark report
- Ability to create static graph images based on the result data using plotly/orca (see examples below)
- No ssh access required, just an access to the target cluster through **standard kubectl**
- Custom kubeconfig file can be specified as a parameter
- **No need for high privileges**, the script will just launch very lightweight pods on two nodes.
- Based on **very lights containers** images :
  - ![Docker Image Size (tag)](https://img.shields.io/docker/image-size/infrabuilder/bench-iperf3/latest) [infrabuilder/bench-iperf3](https://hub.docker.com/r/infrabuilder/bench-iperf3), is used to run benchmark tests
  - ![Docker Image Size (tag)](https://img.shields.io/docker/image-size/infrabuilder/bench-custom-monitor/latest) [infrabuilder/bench-custom-monitor](https://hub.docker.com/r/infrabuilder/bench-custom-monitor), is used to monitor nodes
- **Ability to run the whole suite in a container** [olegeech/k8s-bench-suite](https://hub.docker.com/r/olegeech/k8s-bench-suite):
  - Image is based on the bitnami/kubectl
  - Nodes for testing can be auto-preselected

### Requirements 

This script needs a valid `kubectl` setup with an access to the target cluster.

Binaries dependencies for the host that will execute [knb](knb) :

- awk
- grep
- tail
- date
- kubectl
- jq (for plotting)

### Quickstart

Choose two nodes to act as server/client on your cluster (for example node1 and node2) . Then start the knb : 

```bash
./knb --verbose --client-node node1 --server-node node2
```

If you omit the `--verbose` flag, it will also complete, but you will have no output until the end of the benchmark.

### Docker quickstart

**Environment variables:**

- `NODE_AUTOSELECT` Auto-selects a few nodes from cluster for running tests
- `MASTER_ELIGIBLE` Master nodes can also be chosen

You need to mount a valid kubeconfig inside the container and provide all other required flags to knb:

```bash
docker run -e NODE_AUTOSELECT=1 -it --hostname knb --name knb --rm -v /home/user/my-graphs:/my-graphs -v /path/to/my/kubeconfig:/.kube/config olegeech/k8s-bench-suite --verbose --plot --plot-dir /my-graphs
```

### Examples

- Simple benchmark from "node1" to "node2" in **verbose** mode :

  ```bash
  knb -v -cn node1 -sn node2
  ```

- Benchmark from "nA" to "nB" and **save data** in file `mybench.knbdata` 

  ```bash 
  knb -cn nA -sn nB -o data -f mybench.knbdata
  ```

- Generate report **in json** from **previous benchmark** data file `mybench.knbdata`

  ```bash
  knb -fd mybench.knbdata -o json
  ```

- Plot graphs from **previous benchmark** data file `mybench.knbdata`

  ```bash
  knb -fd mybench.knbdata --plot --plot-args '--width 900 --height 600'
  ```

- To run benchmark from node A to node B, showing only result **in yaml** format : 

  ```bash
  knb -cn A -sn B -o yaml
  ```

- To run benchmark from node Asterix to node Obelix, with the **most verbose output** and a result as **json** in a `res.json` file :

  ```bash
  knb --debug -cn Asterix -sn Obelix -o json -f res.json
  ```

- Running benchmark **in namespace** `myns` :

  ```bash
  knb -n myns -cn node1 -sn node2
  ```

- Run **only idle and tcp** benchmark :

  ```bash
  knb -cn clientnode -sn servernode -ot idle,tcp
  ```

### Usage

To display usage, use the `-h` flag :

```bash
aducastel@infrabuilder:~/k8s-bench-suite$ ./knb -h

knb is a network benchmark tool for Kubernetes CNI

There are two modes :
- benchmark mode : will actually run benchmark on a cluster
- from data mode : read data generated by previous benchmark with "-o data" flag

=====[ Benchmark mode ]====================================================

 Mandatory flags :

    -cn <nodename>
    --client-node <nodename>    : Define kubernetes node name that will host the client part

    -sn <nodename>
    --server-node <nodename>    : Define kubernetes node name that will host the server part

 Optionnal flags :
    -d <time-in-scd>
    --duration <time-in-scd>    : Set the benchmark duration for each test in seconds (Default 10)

    -k
    --keep                      : Keep data directory instead of cleaning it (tmp dir that contains raw benchmark data)

    -n <namespace>
    --namespace <namespace>     : Set the target kubernetes namespace

    --name <name>               : Set the name of this benchmark run

    -ot <testlist>
    --only-tests <testlist>     : Only run a subset of benchmark tests, comma separated (Ex: -ot tcp,idle)
                                  Possible values: all, tcp, udp, p2p, p2s , p2ptcp, p2pudp, p2stcp, p2sudp, idle

    -sbs <size>
    --socket-buffer-size <size> : Set the UDP socket buffer size with unit, or 'auto'. ex: '256K' (Default: auto)

    -t <time-in-scd>
    --timeout <time-in-scd>     : Set the pod ready wait timeout in seconds (Default 30)

=====[ From Data mode ]====================================================

Mandatory flags :
    -fd <path>
    --from-data <path>          : Define the path to the data to read from
                                  Data file must be rendered with '--output data'

=====[ Common optionnal flags ]============================================

    --debug                     : Set the debug level to "debug"

    -dl <level>
    --debug-level <level>       : Set the debug level
                                  Possible values: standard, warn, info, debug

    -f <filepath>
    --file <filepath>           : Set the output file

    -h
    --help                      : Display this help message

    -p
    --plot                      : Plot data using plotly/orca

    -pd
    --plot-dir                  : Directory where to save graphs
                                  Defaults to the current directory

    -pa
    --plot-args                 : Arguments to the plotly's 'orca graph' function
                                  Defaults to '--width 900 --height 500'

    -o <format>
    --output <format>           : Set the output format. Defaults to 'text'
                                  Possible values: text, yaml, json, data
    -v
    --verbose                   : Activate the verbose mode by setting debug-level to 'info'

    -V
    --version                   : Show current script version

    Added for ATLAS benchmarks :

		-hns
		--host-name-server          : Set server's hostNetwork to True (Default $HOST_NETWORK_SERVER) 

		-hnc
		--host-network-client		    : Set client's hostNetwork to True (Default $HOST_NETWORK_CLIENT)

		-acmd
		--additional-command		    : Used to pass additional commands to run on the client pod

    -ccmd
		--custom-command			      : Custom command to be executed by the Client Pod

=====[ Examples ]==========================================================

  Simple benchmark from "node1" to "node2" in verbose mode
  -------------------------------------------------------------------------
  | knb -v -cn node1 -sn node2                                            |
  -------------------------------------------------------------------------

  Benchmark from "nA" to "nB" with data saved in file "mybench.knbdata"
  -------------------------------------------------------------------------
  | knb -cn nA -sn nB -o data -f mybench.knbdata                          |
  -------------------------------------------------------------------------

  Generate report in json from previous benchmark file "mybench.knbdata"
  -------------------------------------------------------------------------
  | knb -fd mybench.knbdata -o json                                       |
  -------------------------------------------------------------------------

  Create graph images from previous benchmark file "mybench.knbdata"
  -------------------------------------------------------------------------
  | knb -fd mybench.knbdata  --plot --plot-dir ./my-graphs                |
  -------------------------------------------------------------------------

  Run only idle and tcp benchmark :
  -------------------------------------------------------------------------
  | knb -cn clientnode -sn servernode -ot idle,tcp                        |
  -------------------------------------------------------------------------

```

## [KNB Autotester](autotester.py) : KNB Autotester

Autotester is a Python script created to help automate multiple network tests. It runs knb script mutilple times, according to the configuration file. 

This script was created by Filip Katulski <filip.katulski@cern.ch>

Here are some highlights:

- **Plain Python3 script** with very few dependencies
- Runs knb script accordingly to the specified YAML configuration file
- Ability to select multiple Server-Client pairs
- Saves results in the specified location
- Can run multiple custom tests
- Can run specified combination of basic tests with all additional parameters possible
- Option to create data plots from data folder specified by YAML configuration file
- **No need for high privileges**

### Requirements 

This script needs valid **kubectl** setup and has **all requirements of [knb](knb) script** and additionally:

- PyYAML
- art (for art message)

### Examples

- Simple benchmark of files specified in **config.yaml** file:

  ```bash
  python3 autotester.py -i config.yaml
  ```

- Simple data plotting accordingly to **plotconf.yaml** file :

  ```bash
  python3 autotester.py -p -i plotconf.yaml 
  ```

- knb script usage message :

  ```bash
  python3 autotester.py -k
  ```

### Usage

To display usage, use the `-h` flag :

```bash
knb is a network benchmark tool for Kubernetes CNI.
Autotester script is used to automate running multiple knb tests one by one or create plots for multiple tests,
according to provided yaml files.
The output testing data is saved to a tar file. Test names as combination '<server>-<client>-<customtestindex>.knbtest'.
The output plots are png files saved in the directory named after the test, at the specified location.

==========
PARAMETERS
==========

    -h, --help                  | displays this  help message

    -k, --knb-help              | displays knb script help message
    
    -i, --input <filename>      | input yaml file with test or plotting configuration

    -p, --plot                  | switches to plotting mode

=======
TESTING
=======

Required parameters are:
- "server, client" pairs 
- namespace
- output-folder

Optional parameters:
- individual specified servers and clients for grid testing
- basic-tests
- custom-tests
- optional
- kubeconfig-file

To see the full description of parameters required by knb script please use "-k" flag.

Input test specification yaml file should follow this structure:
_________________________________________________
nodes:
  pairs:
    - server-1, client-1
    - server-2, client-2
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
    "/path/to/kubeconfig/file"

_________________________________________________

```

## KNB plotting module examples

![bandwidth](https://user-images.githubusercontent.com/21361354/102022246-d6e1d080-3d85-11eb-8ca6-37064ac3918f.png)
![cpu-usage](https://user-images.githubusercontent.com/21361354/102022247-d812fd80-3d85-11eb-820f-f5108cf8b930.png)
![ram-usage](https://user-images.githubusercontent.com/21361354/102022250-d812fd80-3d85-11eb-9f1b-650571bb0054.png)

