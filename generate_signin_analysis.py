#!/usr/bin/python

import sys

from included_to_including_analyzer import IncludedToIncludingAnalyzer
from including_to_included_analyzer import IncludingToIncludedAnalyzer
import common_utils
import signin_analysis_lib


def GenerateAnalysis(database_filename):
  including_analyzer = (
      IncludingToIncludedAnalyzer(database_filename,
                                  signin_analysis_lib.INCLUDING_FILE_FILTERS))
  output_csv = including_analyzer.GenerateGlobalAnalysisAsCsv(
      signin_analysis_lib.FilenameToSigninClient, "feature")
  print output_csv

  signin_analysis = including_analyzer.GenerateAnalysis(
      lambda f: signin_analysis_lib.InClient(f, "signin"))
  print common_utils.DictToCsv(
      signin_analysis, ["file", "num inclusions"],
      common_utils.DictKeysSortedByValue(signin_analysis))

  included_analyzer = (
      IncludedToIncludingAnalyzer(database_filename,
                                  signin_analysis_lib.INCLUDING_FILE_FILTERS))
  included_files_analysis = included_analyzer.GenerateAnalysis()
  print common_utils.DictToCsv(
      included_files_analysis, ["file", "num inclusions"],
      common_utils.DictKeysSortedByValue(included_files_analysis))

if __name__ == '__main__':
  database_path = sys.argv[1]
  GenerateAnalysis(database_path)
