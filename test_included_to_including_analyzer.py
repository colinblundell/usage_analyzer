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
  def CreateAnalyzer(self, including_file_filters):
    with common_utils.TemporaryDirectory() as output_dir:
      # TODO: Should I have a test database that I read off disk?
      config_filename = (
          "./test/data/configs/test_included_to_including_analyzer_config.py")
      generate_inclusions.generate_inclusions(config_filename, output_dir)

      repo_rev = git_utils.GetUsageAnalyzerRepoRevision()
      database_name = "_".join(["test", repo_rev, "inclusions_db.py"])
      database_filepath = os.path.join(output_dir, "test", repo_rev,
                                       database_name)
      assert os.path.isfile(database_filepath)

      analyzer = IncludedToIncludingAnalyzer(database_filepath,
                                             including_file_filters)
    return analyzer

  def test_GenerateAnalysis(self):
    analyzer = self.CreateAnalyzer([])

    # Test with a filter that allows all including files.
    expected_output = {"total": 3,
                       "foo/foo.h": 1,
                       "bar/core.h": 2}
    output = analyzer.GenerateAnalysis()
    self.assertEqual(expected_output, output)
