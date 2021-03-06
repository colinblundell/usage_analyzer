import os
import unittest

import common_utils
import generate_inclusions
import git_utils
import inclusions_config
import inclusions_database
from included_to_including_analyzer import IncludedToIncludingAnalyzer


class TestGenerateIncludedToIncludingAnalyzer(unittest.TestCase):
  # Creates an IncludedToIncludingAnalyzer instance that operates on
  # the test config associated with these tests and |including_file_filters|.
  def CreateAnalyzer(self,
                     including_file_filters,
                     included_files_to_limit_to=None):
    with common_utils.TemporaryDirectory() as output_dir:
      # TODO: Should I have a test database that I read off disk?
      config_filename = (
          "./test/data/configs/test_included_to_including_analyzer_config.py")
      generate_inclusions.generate_inclusions("dummy", config_filename,
                                              output_dir)

      repo_rev = git_utils.GetUsageAnalyzerRepoRevision()
      database_name = "_".join(["test", repo_rev, "inclusions_db.py"])
      database_filepath = os.path.join(output_dir, "test", repo_rev,
                                       database_name)
      assert os.path.isfile(database_filepath)

      analyzer = IncludedToIncludingAnalyzer(
          database_filepath,
          including_file_filters,
          included_files_to_limit_to=included_files_to_limit_to)
    return analyzer

  def test_LimitIncludedFiles(self):
    analyzer = self.CreateAnalyzer([], ["bar/core.h"])
    expected_included_file_dict = {
        "bar/core.h": ["bar/baz/bar_core_factory.h", "bar/bar.h"]
    }
    self.assertEqual(expected_included_file_dict, analyzer.included_file_dict)

  def test_GenerateAnalysisDefaultFilter(self):
    # Test with a filter that allows all including files.
    analyzer = self.CreateAnalyzer([])

    expected_output = {"total": 3, "foo/foo.h": 1, "bar/core.h": 2}
    output = analyzer.GenerateAnalysis()
    self.assertEqual(expected_output, output)

  def test_GenerateAnalysisCustomFilter(self):
    # Test with a filter that filters out bar/bar.*.
    analyzer = self.CreateAnalyzer(["bar/bar\..*"])

    expected_output = {"total": 1, "foo/foo.h": 0, "bar/core.h": 1}
    output = analyzer.GenerateAnalysis()
    self.assertEqual(expected_output, output)
