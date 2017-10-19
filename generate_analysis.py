#!/usr/bin/python

import os
import sys

import common_utils
import inclusions_config
import inclusions_database

CLIENTS = [
"ios/web_view/internal/signin",
"arc/auth",
"login",
"sync",
"signin",
"history",
"autofill",
"password",
"policy",
"supervised_user",
"gcm",
# NOTE: This should be below sync and gcm to avoid catching their driver dirs.
"drive",
"invalidation",
"ntp_snippets",
"suggestions",
"profiles",
"google_apis",
"settings",
"payments",
"cryptauth",
"first_run",
"bookmarks",
"api/identity",
"webui",
"ios/chrome/browser/ui",
"chrome/browser/ui",
"chrome/browser/extensions",
"extensions",
]

def signin_clients_partition_function(filename):
  for client in CLIENTS:
    if client in filename:
      return client

  return os.path.dirname(filename)

def generate_analysis(database_filename):
  inclusions_db = inclusions_database.read_inclusions_db_from_disk(
    database_filename)

  # Eliminate inclusions coming from included files.
  including_file_dict = inclusions_database.filter_out_included_files_as_keys(
    inclusions_db)

  # Eliminate inclusions coming from the Identity Service.
  identity_service_regex = "^services/identity/.*"
  including_file_dict = common_utils.dict_filter_keys_matching_regex(
    including_file_dict, [identity_service_regex])

  including_file_dict = common_utils.dict_list_values_to_sums(
    including_file_dict)

  feature_groups = common_utils.dict_partition_keys(
    including_file_dict, signin_clients_partition_function)
  feature_dict = {}
  for feature, including_files in feature_groups.items():
    feature_dict[feature] = 0
    for including_file in including_files:
      feature_dict[feature] += including_file_dict[including_file]

  # Prepare |feature_dict| for display.
  feature_dict = common_utils.dict_with_total(feature_dict)

  field_names = ["signin client", "num inclusions"]
  key_order = common_utils.dict_keys_sorted_by_value(feature_dict)
  output_csv = common_utils.dict_to_csv(feature_dict, field_names, key_order)
  print output_csv

if __name__ == '__main__':
  database_filename = sys.argv[1]
  generate_analysis(database_filename)
