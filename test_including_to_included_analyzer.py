import os
import unittest

import common_utils
import generate_inclusions
import git_utils
import inclusions_config
import inclusions_database
from including_to_included_analyzer import IncludingToIncludedAnalyzer


class TestGenerateIncludingToIncludedAnalyzer(unittest.TestCase):
  # Creates an IncludingToIncludedAnalyzer instance that operates on
  # the test config associated with these tests and uses
  # |including_file_filters|.
  def CreateAnalyzer(self, including_file_filters):
    with common_utils.TemporaryDirectory() as output_dir:
      # TODO: Should I have a test database that I read off disk?
      config_filename = (
          "./test/data/configs/test_including_to_included_analyzer_config.py")
      generate_inclusions.generate_inclusions(config_filename, output_dir)

      repo_rev = git_utils.GetUsageAnalyzerRepoRevision()
      database_name = "_".join(["test", repo_rev, "inclusions_db.py"])
      database_filepath = os.path.join(output_dir, "test", repo_rev,
                                       database_name)
      assert os.path.isfile(database_filepath)

      analyzer = IncludingToIncludedAnalyzer(database_filepath,
                                             including_file_filters)
    return analyzer

  def test_GenerateAnalysis(self):
    analyzer = self.CreateAnalyzer([])
    expected_output = {"total": 3,
                       "bar/bar.h": 2,
                       "bar/baz/bar_core_factory.h": 1}
    output = analyzer.GenerateAnalysis()
    self.assertEqual(expected_output, output)

  def test_GenerateGlobalAnalysisForFiltersDefaultFilters(self):

    def KeyPartitionFunction(filename):
      return os.path.dirname(filename)

    analyzer = self.CreateAnalyzer([])
    expected_output = {"total": 3, "bar": 2, "bar/baz": 1}
    output = analyzer.GenerateGlobalAnalysisForFilters(KeyPartitionFunction)
    self.assertEqual(expected_output, output)

  def test_GenerateGlobalAnalysisForFiltersConstructionFilter(self):

    def KeyPartitionFunction(filename):
      return os.path.dirname(filename)

    analyzer = self.CreateAnalyzer([r"bar/baz.*"])
    expected_output = {"total": 2, "bar": 2}
    output = analyzer.GenerateGlobalAnalysisForFilters(KeyPartitionFunction)
    self.assertEqual(expected_output, output)

  def test_GenerateGlobalAnalysisForFiltersMultipleFilters(self):

    def KeyPartitionFunction(filename):
      return os.path.dirname(filename)

    analyzer = self.CreateAnalyzer([r"bar/baz.*"])
    expected_output = {"total": 0}
    output = analyzer.GenerateGlobalAnalysisForFilters(
        KeyPartitionFunction, filters=["bar/bar\..*"])
    self.assertEqual(expected_output, output)

  def test_GenerateGlobalAnalysis(self):

    def KeyPartitionFunction(filename):
      return os.path.dirname(filename)

    analyzer = self.CreateAnalyzer([])
    expected_all_inclusions = {"total": 3, "bar": 2, "bar/baz": 1}
    expected_prod_inclusions = {"total": 3, "bar": 2, "bar/baz": 1}
    expected_prod_non_factory_inclusions = {"total": 2, "bar": 2}
    expected_output = [["all", expected_all_inclusions], [
        "prod", expected_prod_inclusions
    ], ["prod non-factory", expected_prod_non_factory_inclusions]]
    output = analyzer.GenerateGlobalAnalysis(KeyPartitionFunction)
    self.assertEqual(expected_output, output)

  def test_GenerateGlobalAnalysisAsCsv(self):

    def KeyPartitionFunction(filename):
      return os.path.dirname(filename)

    analyzer = self.CreateAnalyzer([])
    expected_output = "key name,all,prod,prod non-factory\r\n"
    expected_output += "total,3,3,2\r\n"
    expected_output += "bar,2,2,2\r\n"
    expected_output += "bar/baz,1,1,0\r\n"
    output = analyzer.GenerateGlobalAnalysisAsCsv(KeyPartitionFunction,
                                                  "key name")
    self.assertEqual(expected_output, output)
