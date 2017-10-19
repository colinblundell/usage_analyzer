#!/usr/bin/python

import os
import sys

import common_utils
import inclusions_config
import inclusions_database

def generate_analysis(database_filename):
  inclusions_db = inclusions_database.read_inclusions_db_from_disk(
    database_filename)
  including_files_to_included_files = ( 
    inclusions_db["including_files_to_included_files"])
  output_dict = common_utils.dict_list_values_to_sums(
    including_files_to_included_files)
  output_dict["total"] = sum([v for v in output_dict.values()])
  field_names = ["including file", "num inclusions"]
  key_order = common_utils.dict_keys_sorted_by_value(output_dict)
  output_csv = common_utils.dict_to_csv(output_dict, field_names, key_order)
  print output_csv

if __name__ == '__main__':
  database_filename = sys.argv[1]
  generate_analysis(database_filename)
