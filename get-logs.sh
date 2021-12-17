#!/bin/bash
###################################################################
# @Description : Logging tool for K8s Bench Suite
# @Author      : Filip Katulski <filip.katulski@cern.ch>
# @License     : Beerware
###################################################################

#                          WORK IN PROGRESS

###################################################################

function usage {
	cat <<-EOF

	Possible flags:

        -h
	    --help                      : Display this help message

        -p
        --pod                       : Pod name

        -n
        --namespace                 : Namespace

EOF
}

[ "$1" = "" ] && usage && exit

UNKNOWN_ARGLIST=""
while [ "$1" != "" ]
do
	arg=$1
	case $arg in
		#--- Benchmark mode - Mandatory flags ---------------------------------

		# Define kubernetes node name that will host the client part
		--pod|-p)
			shift
			[ "$1" = "" ] && fatal "$arg flag must be followed by a value"
			POD_NAME=$1
			info "Server node will be '$POD_NAME'"
			;;

		# Define kubernetes node name that will host the server part
		--namespace|-n)
			shift
			[ "$1" = "" ] && fatal "$arg flag must be followed by a value"
			NAMESPACE=$1
			info "Client node will be '$NAMESPACE'"
			;;

        --help|-h)
			usage && exit
			;;

        esac
    shift
done

[ "$UNKNOWN_ARGLIST" != "" ] && fatal "Unknown arguments : $UNKNOWN_ARGLIST"
$DEBUG && debug "Argument parsing done"

kubectl describe -n $NAMESPACE pod $POD_NAME > ./temp-logs/runbooks_describe_pod.txt
kubectl logs -p $POD_NAME -n $NAMESPACE > ./temp-logs/runbooks_pod_logs.txt
kubectl logs -p $POD_NAME --previous -n $NAMESPACE > ./temp-logs/runbooks_previous_pod_logs.txt
