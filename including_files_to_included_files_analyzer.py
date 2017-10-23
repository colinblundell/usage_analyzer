#!/usr/bin/python

import os

import common_utils
import inclusions_database

# Regexes that filter out test files, leaving only prod files.
PROD_FILTERS = [".*fake.*", ".*test.*"]

# Regexes that filter both test files and factories.
PROD_NON_FACTORY_FILTERS = PROD_FILTERS + [".*_factory.*"]


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

  # Generates a global analysis of |self.including_file_dict| and |filters| as
  # follows:
  # Filters |self.including_file_dict| by |filters|.
  # Partitions including files into features based on |key_partition_function|.
  # Produces a dictionary whose keys are features and whose values are the
  # sums of the total inclusions of all including files within those features.
  # Augments the dictionary with the total number of inclusions.
  # Returns the produced dictionary.
  # Note that by default, |filters| is [], i.e., no custom filters are applied.
  def generate_global_analysis_for_filters(self,
                                           key_partition_function,
                                           filters=[]):
    including_file_dict = common_utils.dict_filter_keys_matching_regex(
        self.including_file_dict, filters)

    feature_groups = common_utils.dict_partition_keys(including_file_dict,
                                                      key_partition_function)

    feature_dict = {}
    including_file_dict = common_utils.dict_list_values_to_sums(
        including_file_dict)
    for feature, including_files in feature_groups.items():
      feature_dict[feature] = 0
      for including_file in including_files:
        feature_dict[feature] += including_file_dict[including_file]

    feature_dict = common_utils.dict_with_total(feature_dict)
    return feature_dict

  # Generates a global analysis of |self.including_file_dict| as follows:
  # Partitions including files into features based on |key_partition_function|.
  # Produces global analyses for:
  # (1) all inclusions
  # (2) all inclusions from prod files
  # (3) all inclusions from non-factory prod files
  # Returns a list of pairs where the first element is an identifier for the
  # analysis and the second element is the dictionary representing the analysis
  # itself.
  def generate_global_analysis(self, key_partition_function):
    feature_dicts = []
    including_files_filters = [["all", []], ["prod", PROD_FILTERS],
                               ["prod non-factory", PROD_NON_FACTORY_FILTERS]]

    for name, filters in including_files_filters:
      feature_dict = self.generate_global_analysis_for_filters(
          key_partition_function, filters=filters)
      feature_dicts.append([name, feature_dict])
    return feature_dicts

  # Generates a global analysis as described above and returns a string
  # representing that global analysis in CSV format. |key_header_name| is
  # used in the CSV's header as the name for the column of keys.
  def generate_global_analysis_as_csv(self, key_partition_function,
                                      key_header_name):
    global_analysis = self.generate_global_analysis(key_partition_function)
    presentation_order, feature_dicts = zip(*global_analysis)
    key_order = common_utils.dict_keys_sorted_by_value(feature_dicts[0])
    feature_dicts = common_utils.dicts_with_missing_entries_filled(
        feature_dicts, key_order, 0)
    field_names = [key_header_name] + list(presentation_order)
    output_csv = common_utils.dicts_to_csv(feature_dicts, field_names,
                                           key_order)
    return output_csv
