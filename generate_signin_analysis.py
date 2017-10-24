#!/usr/bin/python

import sys

from including_to_included_analyzer import IncludingToIncludedAnalyzer
import signin_analysis_lib


def GenerateAnalysis(database_filename):
  analyzer = (
      IncludingToIncludedAnalyzer(database_filename,
                                  signin_analysis_lib.INCLUDING_FILE_FILTERS))
  output_csv = analyzer.GenerateGlobalAnalysisAsCsv(
      signin_analysis_lib.FilenameToSigninClient, "feature")
  print output_csv
  print


if __name__ == '__main__':
  database_path = sys.argv[1]
  GenerateAnalysis(database_path)
