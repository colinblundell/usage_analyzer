#!/usr/bin/python

import os
import sys

from included_to_including_analyzer import IncludedToIncludingAnalyzer
from including_to_included_analyzer import IncludingToIncludedAnalyzer
import common_utils
import signin_analysis_lib


def GenerateAnalysis(database_filename):
  output_dir = os.path.join(os.path.dirname(database_filename), "analyses")
  if not os.path.exists(output_dir):
    os.mkdir(output_dir)

  including_analyzer = (
      IncludingToIncludedAnalyzer(database_filename,
                                  signin_analysis_lib.INCLUDING_FILE_FILTERS))

  features_analysis_csv = including_analyzer.GenerateGlobalAnalysisAsCsv(
      signin_analysis_lib.FilenameToSigninClient, "feature")
  features_analysis_filename = os.path.join(output_dir, "features_analysis.txt")
  with open(features_analysis_filename, "w") as f:
    f.write(features_analysis_csv)

  signin_analysis = including_analyzer.GenerateAnalysis(
      lambda f: signin_analysis_lib.InClient(f, "signin"))
  signin_analysis_csv = common_utils.DictToCsv(
      signin_analysis, ["file", "num inclusions"],
      common_utils.DictKeysSortedByValue(signin_analysis))
  signin_analysis_filename = os.path.join(output_dir,
                                          "signin_feature_analysis.txt")
  with open(signin_analysis_filename, "w") as f:
    f.write(signin_analysis_csv)

  included_analyzer = (
      IncludedToIncludingAnalyzer(database_filename,
                                  signin_analysis_lib.INCLUDING_FILE_FILTERS))
  included_files_analysis = included_analyzer.GenerateAnalysis()
  included_files_analysis_csv = common_utils.DictToCsv(
      included_files_analysis, ["file", "num inclusions"],
      common_utils.DictKeysSortedByValue(included_files_analysis))
  included_files_analysis_filename = os.path.join(output_dir,
                                                  "included_files_analysis.txt")
  with open(included_files_analysis_filename, "w") as f:
    f.write(included_files_analysis_csv)


if __name__ == '__main__':
  database_path = sys.argv[1]
  GenerateAnalysis(database_path)
