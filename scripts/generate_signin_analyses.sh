#!/bin/bash

# This script exists to generate analyses for the signin databases.
analysis_configs=`data/analysis_configs/*`

for database in `ls ./data/databases/signin_internals`; do
  generate_analysis_base="./generate_signin_analysis.py $HOME/usage_analyzer/data/databases/signin_internals/$database/signin_internals_${database}_inclusions_db.py"

  # Generate the overall analysis.
  $generate_analysis_base

  # For each config to be analyzed, generate its analysis.
  for config in $analysis_configs; do
    $generate_analysis_base $config
  done

done
