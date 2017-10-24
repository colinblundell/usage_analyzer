#!/usr/bin/python

import sys

from including_to_included_analyzer import IncludingToIncludedAnalyzer
import common_utils
import signin_analysis_lib


def GenerateAnalysis(database_filename):
  analyzer = (
      IncludingToIncludedAnalyzer(database_filename,
                                  signin_analysis_lib.INCLUDING_FILE_FILTERS))
  output_csv = analyzer.GenerateGlobalAnalysisAsCsv(
      signin_analysis_lib.FilenameToSigninClient, "feature")
  print output_csv

  signin_analysis = analyzer.GenerateAnalysis(lambda f: signin_analysis_lib.InClient(f, "signin"))
  print common_utils.DictToCsv(signin_analysis, ["file", "num inclusions"], common_utils.DictKeysSortedByValue(signin_analysis))


if __name__ == '__main__':
  database_path = sys.argv[1]
  GenerateAnalysis(database_path)
