#!/usr/bin/python

import os
import sys

import common_utils
from including_files_to_included_files_analyzer import IncludingFilesToIncludedFilesAnalyzer
import inclusions_config
import inclusions_database
import signin_analysis_lib

def generate_analysis(database_filename):
  analyzer = (IncludingFilesToIncludedFilesAnalyzer(database_filename,
    signin_analysis_lib.INCLUDING_FILE_FILTERS))

  feature_dict = analyzer.generate_global_feature_analysis(
    signin_analysis_lib.filename_to_signin_client)

  field_names = ["signin client", "num inclusions"]
  key_order = common_utils.dict_keys_sorted_by_value(feature_dict)
  output_csv = common_utils.dict_to_csv(feature_dict, field_names, key_order)
  print output_csv

if __name__ == '__main__':
  database_filename = sys.argv[1]
  generate_analysis(database_filename)
