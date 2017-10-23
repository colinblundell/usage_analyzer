import os
import unittest

import common_utils
import generate_inclusions
import git_utils
import inclusions_config
import inclusions_database
from including_files_to_included_files_analyzer import IncludingFilesToIncludedFilesAnalyzer

class TestGenerateIncludingFilesToIncludedFilesAnalyzer(unittest.TestCase):
  # Creates an IncludingFilesToIncludedFilesAnalyzer instance that operates on
  # the test config associated with these tests and uses
  # |including_file_filters|.
  def create_analyzer(self, including_file_filters):
    with common_utils.TemporaryDirectory() as output_dir:
      # TODO: Should I have a test database that I read off disk?
      config_filename = "./test/data/configs/test_including_files_to_included_files_analyzer_config.py"
      generate_inclusions.generate_inclusions(config_filename, output_dir)

      repo_rev = git_utils.get_usage_analyzer_repo_revision()
      database_name = "_".join(["test", repo_rev, "inclusions_db.py"])
      database_filepath = os.path.join(output_dir, "test", repo_rev, 
                                       database_name)
      assert os.path.isfile(database_filepath)

      analyzer = IncludingFilesToIncludedFilesAnalyzer(database_filepath,
        including_file_filters)
    return analyzer

  def test_generate_global_analysis_for_filters_default_filter(self):
      def key_partition_function(filename):
        return os.path.dirname(filename)

      analyzer = self.create_analyzer([])
      expected_output = {"total" : 3, "bar" : 2, "bar/baz" : 1}
      output = analyzer.generate_global_analysis_for_filters(key_partition_function)
      self.assertEqual(expected_output, output)

  def test_generate_global_analysis_for_filters_custom_filter(self):
      def key_partition_function(filename):
        return os.path.dirname(filename)

      analyzer = self.create_analyzer([r"bar/baz.*"])
      expected_output = {"total" : 2, "bar" : 2}
      output = analyzer.generate_global_analysis_for_filters(key_partition_function)
      self.assertEqual(expected_output, output)

  def test_generate_global_analysis_for_filters_multiple_custom_filters(self):
      def key_partition_function(filename):
        return os.path.dirname(filename)

      analyzer = self.create_analyzer([r"bar/baz.*"])
      expected_output = {"total" : 0}
      output = analyzer.generate_global_analysis_for_filters(key_partition_function,
        extra_including_files_filters=["bar/bar\..*"])
      self.assertEqual(expected_output, output)
