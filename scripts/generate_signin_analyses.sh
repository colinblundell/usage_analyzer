#!/bin/bash

# This script exists to generate analyses for the signin databases.
usage_analyzer_home=`dirname $0`/..
analysis_configs=`ls ${usage_analyzer_home}/data/analysis_configs/signin/*`

for database in `ls ${usage_analyzer_home}/data/databases/signin_internals`; do
  generate_analysis_base="${usage_analyzer_home}/generate_signin_analysis.py ${usage_analyzer_home}/data/databases/signin_internals/$database/signin_internals_${database}_inclusions_db.py"

  # Generate the overall analysis.
  $generate_analysis_base

  # For each config to be analyzed, generate its analysis.
  for config in $analysis_configs; do
    $generate_analysis_base $config
  done

done
