#!/usr/bin/python

import copy
import os
import sys

from included_to_including_analyzer import IncludedToIncludingAnalyzer
from including_to_included_analyzer import IncludingToIncludedAnalyzer
import common_utils
import signin_analysis_lib

individual_feature_analyses = ["signin"]


def GenerateAnalyses(database_filename):
  output_dir = os.path.join(os.path.dirname(database_filename), "analyses")
  if not os.path.exists(output_dir):
    os.mkdir(output_dir)

  including_analyzer = (
      IncludingToIncludedAnalyzer(database_filename,
                                  signin_analysis_lib.INCLUDING_FILE_FILTERS))

  features_num_inclusions_csv = including_analyzer.GenerateGroupAnalysisAsCsv(
      "num_inclusions", signin_analysis_lib.FilenameToSigninClient, "feature")
  features_num_inclusions_filename = os.path.join(output_dir,
                                                  "features_num_inclusions.txt")
  with open(features_num_inclusions_filename, "w") as f:
    f.write(features_num_inclusions_csv)

  features_num_including_files_csv = including_analyzer.GenerateGroupAnalysisAsCsv(
      "group_size",
      signin_analysis_lib.FilenameToSigninClient,
      "feature",
      key_order=including_analyzer.GroupsOrderedByNumInclusions(
          signin_analysis_lib.FilenameToSigninClient))
  features_num_including_files_filename = os.path.join(
      output_dir, "features_num_including_files.txt")
  with open(features_num_including_files_filename, "w") as f:
    f.write(features_num_including_files_csv)

  for feature in individual_feature_analyses:
    feature_analysis = including_analyzer.GenerateNumInclusionsForFilterFunction(
        lambda f: signin_analysis_lib.InClient(f, feature))
    # Sort files in alphabetical order for the individual feature analysis to
    # group directories together.
    including_files_order = copy.deepcopy(feature_analysis.keys())
    including_files_order.sort()
    feature_analysis_csv = common_utils.DictToCsv(
        feature_analysis, ["file", "# inclusions"], including_files_order)
    feature_analysis_filename = os.path.join(output_dir,
                                             feature + "_feature_analysis.txt")
    with open(feature_analysis_filename, "w") as f:
      f.write(feature_analysis_csv)

  included_analyzer = (
      IncludedToIncludingAnalyzer(database_filename,
                                  signin_analysis_lib.INCLUDING_FILE_FILTERS))
  included_files_analysis = included_analyzer.GenerateAnalysis()
  included_files_order = common_utils.DictKeysSortedByValue(
      included_files_analysis)
  included_files_analysis_csv = common_utils.DictToCsv(
      included_files_analysis, ["file", "# inclusions"], included_files_order)
  included_files_analysis_filename = os.path.join(output_dir,
                                                  "included_files_analysis.txt")
  with open(included_files_analysis_filename, "w") as f:
    f.write(included_files_analysis_csv)


if __name__ == '__main__':
  database_path = sys.argv[1]
  GenerateAnalyses(database_path)
