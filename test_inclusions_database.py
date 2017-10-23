import os
import unittest

import git_utils
import inclusions_database
from test_utils import *


class TestInclusionsDatabase(unittest.TestCase):

  def test_generate_inclusions_database_simple(self):
    output_db = inclusions_database.generate_inclusions_database(
        BASIC_TEST_CONFIG)

    self.assertIn("timestamp (UTC)", output_db)
    self.assertIn("repo_rev", output_db)
    self.assertEqual(output_db["repo_rev"],
                     git_utils.get_usage_analyzer_repo_revision())
    self.assertIn("usage_analyzer_rev", output_db)
    self.assertEqual(output_db["usage_analyzer_rev"],
                     git_utils.get_usage_analyzer_repo_revision())
    self.assertIn("config", output_db)
    self.assertEqual(output_db["config"], BASIC_TEST_CONFIG)
    verify_basic_included_to_including(self, output_db["included_to_including"])
    verify_basic_including_to_included(self, output_db["including_to_included"])

  def test_generate_inclusions_database_complex(self):
    output_db = inclusions_database.generate_inclusions_database(
        COMPLEX_TEST_CONFIG)

    self.assertIn("timestamp (UTC)", output_db)
    self.assertIn("repo_rev", output_db)
    self.assertEqual(output_db["repo_rev"],
                     git_utils.get_usage_analyzer_repo_revision())
    self.assertIn("usage_analyzer_rev", output_db)
    self.assertEqual(output_db["usage_analyzer_rev"],
                     git_utils.get_usage_analyzer_repo_revision())
    self.assertIn("config", output_db)
    self.assertEqual(output_db["config"], COMPLEX_TEST_CONFIG)
    verify_complex_included_to_including(self,
                                         output_db["included_to_including"])
    verify_complex_including_to_included(self,
                                         output_db["including_to_included"])

  def test_filter_out_included_files_as_keys_simple(self):
    db = inclusions_database.generate_inclusions_database(BASIC_TEST_CONFIG)

    output = inclusions_database.filter_out_included_files_as_keys(db)
    expected_output = {"bar/bar.h": ["foo/foo.h"], "bar/core.h": ["foo/foo.h"]}
    self.assertEqual(expected_output, output)

  def test_filter_out_included_files_as_keys_complex(self):
    db = inclusions_database.generate_inclusions_database(COMPLEX_TEST_CONFIG)

    output = inclusions_database.filter_out_included_files_as_keys(db)
    expected_output = {
        "bar/baz/bar_core_factory.h": ["bar/core.h"],
        "foo/foo.h": ["bar/bar.h"]
    }
    self.assertEqual(expected_output, output)
