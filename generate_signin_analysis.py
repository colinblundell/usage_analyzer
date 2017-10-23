#!/usr/bin/python

import sys

from including_to_included_analyzer import IncludingToIncludedAnalyzer
import signin_analysis_lib


def generate_analysis(database_filename):
  analyzer = (
      IncludingToIncludedAnalyzer(database_filename,
                                  signin_analysis_lib.INCLUDING_FILE_FILTERS))
  output_csv = analyzer.generate_global_analysis_as_csv(
      signin_analysis_lib.filename_to_signin_client, "feature")
  print output_csv
  print


if __name__ == '__main__':
  database_filename = sys.argv[1]
  generate_analysis(database_filename)
