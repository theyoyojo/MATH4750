#!/bin/bash

usage() {
echo << DELIMITER
Usage: gather.sh [-o] [-f <output_filename>

-f: specify output filename (defaults to 'data')
-o: overwrite file instead of append

DELIMITER
}

FILENAME="data"
TEE_ARGS="-a"

while getopts "f:a" OPTION; do
        case ${OPTION} in
                f)
			FILENAME="${OPTARG}"
                        ;;
		a)
			GATHER_APPEND=""
			;;
                *)
                        echo "Unknown option ${OPTION}, ignoring"
                        shift
                        ;; esac
done
shift $((OPTIND -1))


# Gather buffered input (instead of using python -u) to allow for Ctl+C
script -qc 'python3 gather.py' | tee ${TEE_ARGS} ${FILENAME}

# We don't actually need this lol
rm -rf "typescript" 

# Remove the ugly ^C from the logfile
sed -i  's/\^C//g' ${FILENAME}
