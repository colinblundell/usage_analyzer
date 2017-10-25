# End-to-end test of generate_inclusions.py.

import datetime
import os
import unittest

import common_utils
import git_utils
import inclusions_config
import inclusions_database
import generate_inclusions

EXPECTED_TEST_CONFIG = {
    'name': 'test',
    'included_files': ['foo/foo.h', 'bar/bar.h'],
    'repo_root': 'test/test_repo'
}
inclusions_config.EvaluateConfig(EXPECTED_TEST_CONFIG)

EXPECTED_INCLUDED_FILES_TO_INCLUDING_FILES = {
    'bar/bar.h': ['foo/foo.h'],
    'foo/foo.h': [
        'foo/foo_unittest.cc', 'foo/foo.cc', 'bar/bar.h', 'bar/core.h'
    ]
}

EXPECTED_INCLUDING_FILES_TO_INCLUDED_FILES = {
    'bar/bar.h': ['foo/foo.h'],
    'bar/core.h': ['foo/foo.h'],
    'foo/foo.cc': ['foo/foo.h'],
    'foo/foo_unittest.cc': ['foo/foo.h'],
    'foo/foo.h': ['bar/bar.h']
}


class TestGenerateInclusions(unittest.TestCase):

  def test_generate_inclusions(self):
    with common_utils.TemporaryDirectory() as output_dir:
      config_filename = "./test/data/configs/test.py"
      generate_inclusions.generate_inclusions(config_filename, output_dir)

      repo_rev = git_utils.GetUsageAnalyzerRepoRevision()
      database_name = "_".join(["test", repo_rev, "inclusions_db.py"])
      database_filepath = os.path.join(output_dir, "test", repo_rev,
                                       database_name)
      assert os.path.isfile(database_filepath)

      inclusions_db = (
          inclusions_database.ReadInclusionsDbFromDisk(database_filepath))

      self.assertEqual(inclusions_db["config"], EXPECTED_TEST_CONFIG)

      self.assertEqual(inclusions_db["included_to_including"],
                       EXPECTED_INCLUDED_FILES_TO_INCLUDING_FILES)
      self.assertEqual(inclusions_db["including_to_included"],
                       EXPECTED_INCLUDING_FILES_TO_INCLUDED_FILES)

      self.assertEqual(inclusions_db["repo_rev"], repo_rev)
      self.assertEqual(inclusions_db["usage_analyzer_rev"], repo_rev)

      timestamp_str = inclusions_db["timestamp (UTC)"]
      timestamp = datetime.datetime.strptime(timestamp_str,
                                             '%Y-%m-%d %H:%M:%S.%f')
      delta = datetime.datetime.utcnow() - timestamp
      self.assertLessEqual(delta, datetime.timedelta(seconds=1))
