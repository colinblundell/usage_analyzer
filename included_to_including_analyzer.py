#!/usr/bin/python

import os

import common_utils
import inclusions_database

# TODO: These need to get put in common location.
# Regexes that filter out test files, leaving only prod files.
common_utils.PROD_FILTERS = [".*fake.*", ".*test.*"]

# Regexes that filter both test files and factories.
common_utils.PROD_NON_FACTORY_FILTERS = common_utils.PROD_FILTERS + [".*_factory.*"]


# Class that can analyze the included_to_including dictionary of an
# inclusions database.
class IncludedToIncludingAnalyzer:
  # Reads an inclusions database from |database_filename| and performs the
  # following filters on its included_to_including dictionary:
  # - Filters out any included files as values.
  # - Filters out values based on the regexes in |including_files_filters|.
  def __init__(self, database_filename, including_files_filters):
    self.inclusions_db = inclusions_database.ReadInclusionsDbFromDisk(
        database_filename)

    included_file_dict = inclusions_database.FilterOutIncludedFilesAsValues(
        self.inclusions_db)
    included_file_dict = common_utils.DictFilterValuesMatchingRegex(
        included_file_dict, including_files_filters)

    self.included_file_dict = included_file_dict

  # Returns a dictionary mapping included files to # of includes,
  # augmented with an entry for the total.
  def GenerateAnalysis(self):
    output_dict = common_utils.DictListValuesToSums(self.included_file_dict)
    output_dict = common_utils.DictWithTotal(output_dict)
    return output_dict
