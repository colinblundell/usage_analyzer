#!/usr/bin/python

import os

import common_utils
import inclusions_database


# Class that can analyze the including_to_included dictionary of an
# inclusions database.
class IncludingToIncludedAnalyzer:
  # Reads an inclusions database from |database_filename| and performs the
  # following filters on its including_to_included dictionary:
  # - Filters out any included files as keys.
  # - Filters out keys based on the regexes in |including_files_filters|.
  # - If |included_files_to_limit_to| is not None, limits the values of the
  #   including_to_included dictionary to elements in that set.
  def __init__(self,
               database_filename,
               including_files_filters,
               included_files_to_limit_to=None):
    self.inclusions_db = inclusions_database.ReadInclusionsDbFromDisk(
        database_filename)

    if included_files_to_limit_to:
      inclusions_database.LimitToSpecifiedIncludedFiles(
          self.inclusions_db, included_files_to_limit_to)

    # TODO: Maybe this function should move to this class?
    including_file_dict = inclusions_database.FilterOutIncludedFilesAsKeys(
        self.inclusions_db)
    including_file_dict = common_utils.DictFilterKeysMatchingRegex(
        including_file_dict, including_files_filters)

    self.including_file_dict = including_file_dict

  # Takes in a filtering function that maps strings to booleans to specify
  # whether the corresponding including files should be included in the
  # analysis. Returns a dictionary mapping filtered including files to # of
  # includes, augmented with an entry for the total.
  def GenerateNumInclusionsForFilterFunction(self, key_filter_function):
    keys = [
        k for k in self.including_file_dict.keys() if key_filter_function(k)
    ]
    output_dict = {}
    for key in keys:
      output_dict[key] = self.including_file_dict[key]
    output_dict = common_utils.DictListValuesToSums(output_dict)
    output_dict = common_utils.DictWithTotal(output_dict)
    return output_dict

  # Generates an analysis of |self.including_file_dict| and |filters| as
  # follows:
  # Filters |self.including_file_dict| by |filters|.
  # Partitions including files into features based on |key_partition_function|.
  # Produces a dictionary whose keys are features and whose values are the
  # sums of the total inclusions of all including files within those features.
  # Augments the dictionary with the total number of inclusions.
  # Returns the produced dictionary.
  # Note that by default, |filters| is [], i.e., no custom filters are applied.
  def GenerateGroupNumInclusionsForFilters(self,
                                           key_partition_function,
                                           filters=None):
    if filters is None:
      filters = []
    including_file_dict = common_utils.DictFilterKeysMatchingRegex(
        self.including_file_dict, filters)

    feature_groups = common_utils.DictPartitionKeys(including_file_dict,
                                                    key_partition_function)

    feature_dict = {}
    including_file_dict = common_utils.DictListValuesToSums(including_file_dict)
    for feature, including_files in feature_groups.items():
      feature_dict[feature] = 0
      for including_file in including_files:
        feature_dict[feature] += including_file_dict[including_file]

    feature_dict = common_utils.DictWithTotal(feature_dict)
    return feature_dict

  # Generates an analysis of |self.including_file_dict| and |filters| as
  # follows:
  # Filters |self.including_file_dict| by |filters|.
  # Partitions including files into features based on |key_partition_function|.
  # Produces a dictionary whose keys are features and whose values are the
  # number of including files within those features.
  # Augments the dictionary with the total number of including files.
  # Returns the produced dictionary.
  # Note that by default, |filters| is [], i.e., no custom filters are applied.
  def GenerateGroupSizesForFilters(self, key_partition_function, filters=None):
    if filters is None:
      filters = []
    including_file_dict = common_utils.DictFilterKeysMatchingRegex(
        self.including_file_dict, filters)

    feature_groups = common_utils.DictPartitionKeys(including_file_dict,
                                                    key_partition_function)

    feature_dict = {}
    for feature, including_files in feature_groups.items():
      feature_dict[feature] = len(including_files)

    feature_dict = common_utils.DictWithTotal(feature_dict)
    return feature_dict

  # Generates an analysis of |self.including_file_dict| as follows:
  # Partitions including files into features based on |key_partition_function|.
  # Produces global analyses for:
  # (1) all inclusions
  # (2) all inclusions from prod files
  # (3) all inclusions from non-factory prod files
  # Returns a list of pairs where the first element is an identifier for the
  # analysis and the second element is the dictionary representing the analysis
  # itself.
  def GenerateGroupNumInclusions(self, key_partition_function):
    feature_dicts = []
    including_files_filters = [["# inclusions", []],
                               ["from prod", common_utils.PROD_FILTERS],
                               [
                                   "from prod non-factory",
                                   common_utils.PROD_NON_FACTORY_FILTERS
                               ]]

    for name, filters in including_files_filters:
      feature_dict = self.GenerateGroupNumInclusionsForFilters(
          key_partition_function, filters=filters)
      feature_dicts.append([name, feature_dict])
    return feature_dicts

  # Partitions including files into features based on |key_partition_function|.
  # Returns these features ordered by the number of inclusions within each
  # feature (in descending order).
  def GroupsOrderedByNumInclusions(self, key_partition_function):
    feature_dict = self.GenerateGroupNumInclusionsForFilters(
        key_partition_function)
    group_order = common_utils.DictKeysSortedByValue(feature_dict)
    return group_order

  # Generates group sizes of |self.including_file_dict| as follows:
  # Partitions including files into features based on |key_partition_function|.
  # Produces group sizes for:
  # (1) all including files
  # (2) all including prod files
  # (3) all including non-factory prod files
  # Returns a list of pairs where the first element is an identifier for the
  # analysis and the second element is the dictionary representing the analysis
  # itself.
  def GenerateGroupSizes(self, key_partition_function):
    feature_dicts = []
    including_files_filters = [["# including files", []],
                               ["prod", common_utils.PROD_FILTERS],
                               [
                                   "prod non-factory",
                                   common_utils.PROD_NON_FACTORY_FILTERS
                               ]]

    for name, filters in including_files_filters:
      feature_dict = self.GenerateGroupSizesForFilters(
          key_partition_function, filters=filters)
      feature_dicts.append([name, feature_dict])
    return feature_dicts

  # Takes in a global analysis and returns a string representing that global
  # analysis in CSV format. |key_header_name| is used in the CSV's header as the
  # name for the column of keys.
  # If |key_order| is not specified, keys will be presented in the order of
  # their values in the first dictionary.
  def GenerateCsvFromGroupAnalysis(self,
                                   analysis,
                                   key_header_name,
                                   key_order=None):
    presentation_order, feature_dicts = zip(*analysis)
    if key_order == None:
      key_order = common_utils.DictKeysSortedByValue(feature_dicts[0])
    feature_dicts = common_utils.DictsWithMissingEntriesFilled(
        feature_dicts, key_order, 0)
    field_names = [key_header_name] + list(presentation_order)
    output_csv = common_utils.DictsToCsv(feature_dicts, field_names, key_order)
    return output_csv

  # Generates a global analysis and returns a string representing that global
  # analysis in CSV format. |key_header_name| is used in the CSV's header as the
  # name for the column of keys.
  # Possible analyses are "num_inclusions" and "group_size".
  # If |key_order| is not specified, keys will be presented in the order of
  # their values in the first dictionary.
  def GenerateGroupAnalysisAsCsv(self,
                                 analysis_type,
                                 key_partition_function,
                                 key_header_name,
                                 key_order=None):
    analysis_types = {
        "num_inclusions": self.GenerateGroupNumInclusions,
        "group_size": self.GenerateGroupSizes,
    }
    analysis_function = analysis_types[analysis_type]
    global_analysis = analysis_function(key_partition_function)
    return self.GenerateCsvFromGroupAnalysis(global_analysis, key_header_name,
                                             key_order)


# Computes the delta between the group num inclusions analyses for
# |database1_filename| and |database2_filename|. Returns this delta in the same
# format as IncludingToIncludedAnalyzer.GenerateGroupNumInclusions(). A key is
# present in each of the returned dictionaries only if its value is non-zero in
# that dictionary.
def ComputeGroupNumInclusionsDeltaBetween(
    database1_filename, database2_filename, key_partition_function):
  analyzer1 = IncludingToIncludedAnalyzer(database1_filename, [])
  analyzer2 = IncludingToIncludedAnalyzer(database2_filename, [])
  group_analysis1 = analyzer1.GenerateGroupNumInclusions(key_partition_function)
  group_analysis2 = analyzer2.GenerateGroupNumInclusions(key_partition_function)
  diff_analysis = []

  for i in range(len(group_analysis1)):
    name = group_analysis1[i][0]
    assert name == group_analysis2[i][0]
    dict1 = group_analysis1[i][1]
    dict2 = group_analysis2[i][1]
    diff = common_utils.DifferenceBetweenDicts(dict1, dict2)
    diff = common_utils.DictWithValueRemoved(diff, 0, keys_to_keep=["total"])
    diff_analysis.append([name, diff])

  return diff_analysis
