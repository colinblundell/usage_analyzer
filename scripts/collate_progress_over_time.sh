#!/bin/bash

# This script exists to run over the analyses for the signin databases and
# provide the collective contents of the progress_over_time_input.txt files
# for pasting into a spreadsheet all in one go. It takes in the analysis config
# to examine.
# NOTE: If desired, the hardcoding to signin_internals here could easily be
# parameterized in the future.

usage_analyzer_home=`dirname $0`/..
analysis_config=$1

NEWLINE=$'\n'
progress_over_time=""
for f in `ls ${usage_analyzer_home}/data/databases/signin_internals` ; do
  progress_over_time+=`cat ${usage_analyzer_home}/data/databases/signin_internals/$f/analyses/$analysis_config/progress_over_time_input.txt`${NEWLINE}
done

echo "$progress_over_time" | sort
