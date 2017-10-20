#!/usr/bin/python

import os

import common_utils
import inclusions_database

# Class that can analyze the including_files_to_included_files dictionary of an
# inclusions database.
class IncludingFilesToIncludedFilesAnalyzer:
  # Reads an inclusions database from |database_filename| and performs the
  # following filters on its including_files_to_included_files dictionary:
  # - Filters out any included files as keys.
  # - Filters out keys based on the regexes in |including_files_filters|.
  def __init__(self, database_filename, including_files_filters):
    self.inclusions_db = inclusions_database.read_inclusions_db_from_disk(
      database_filename)

    # TODO: Maybe this function should move to this class?
    including_file_dict = inclusions_database.filter_out_included_files_as_keys(
      self.inclusions_db)
    including_file_dict = common_utils.dict_filter_keys_matching_regex(
      including_file_dict, including_files_filters)

    self.including_file_dict = including_file_dict

  # Generates a global feature analysis of |self.including_file_dict| as
  # follows:
  # Partitions including files into features based on |key_partition_function|.
  # Produces a dictionary whose keys are features and whose values are the
  # sums of the total inclusions of all including files within those features.
  # Augments the dictionary with the total number of inclusions.
  # Returns the produced dictionary.
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
