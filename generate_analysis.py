#!/usr/bin/python

import os
import sys

import common_utils
import inclusions_config
import inclusions_database

def generate_analysis(database_filename):
  inclusions_db = inclusions_database.read_inclusions_db_from_disk(
    database_filename)

  # Eliminate inclusions coming from included files.
  output_dict = inclusions_database.filter_out_included_files_as_keys(
    inclusions_db)

  # Eliminate inclusions coming from the Identity Service.
  identity_service_regex = "^services/identity/.*"
  output_dict = common_utils.dict_filter_keys_matching_regex(
    output_dict, [identity_service_regex])

  # Prepare |output_dict| for display.
  output_dict = common_utils.dict_list_values_to_sums(
    output_dict)
  output_dict = common_utils.dict_with_total(output_dict)

  field_names = ["including file", "num inclusions"]
  key_order = common_utils.dict_keys_sorted_by_value(output_dict)
  output_csv = common_utils.dict_to_csv(output_dict, field_names, key_order)
  print output_csv

if __name__ == '__main__':
  database_filename = sys.argv[1]
  generate_analysis(database_filename)
