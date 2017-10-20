#!/usr/bin/python

import os

import common_utils
import inclusions_database

class IncludingFilesToIncludedFilesAnalyzer:
  def __init__(self, database_filename, including_files_filters):
    self.inclusions_db = inclusions_database.read_inclusions_db_from_disk(
      database_filename)

    # TODO: Maybe this function should move to this class?
    including_file_dict = inclusions_database.filter_out_included_files_as_keys(
      self.inclusions_db)
    including_file_dict = common_utils.dict_filter_keys_matching_regex(
      including_file_dict, including_files_filters)

    self.including_file_dict = including_file_dict

  def generate_global_feature_analysis(self, key_partition_function):
    feature_groups = common_utils.dict_partition_keys(
      self.including_file_dict, key_partition_function)

    feature_dict = {}
    including_file_dict = common_utils.dict_list_values_to_sums(
      self.including_file_dict)
    for feature, including_files in feature_groups.items():
      feature_dict[feature] = 0
      for including_file in including_files:
        feature_dict[feature] += including_file_dict[including_file]

    feature_dict = common_utils.dict_with_total(feature_dict)
    return feature_dict
