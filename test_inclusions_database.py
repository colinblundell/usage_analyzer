import os
import unittest

import inclusions_database
from test_utils import *

class TestInclusionsDatabase(unittest.TestCase):
  def test_generate_inclusions_database_simple(self):
    output_db = inclusions_database.generate_inclusions_database(
      BASIC_TEST_CONFIG)

    self.assertIn("timestamp (UTC)", output_db)
    self.assertIn("repo_rev", output_db)
    self.assertIn("config", output_db)
    self.assertEqual(output_db["config"], BASIC_TEST_CONFIG)
    verify_basic_included_files_to_including_files(
        self, output_db["included_files_to_including_files"])
    verify_basic_including_files_to_included_files(
        self, output_db["including_files_to_included_files"])

  def test_generate_inclusions_database_complex(self):
    output_db = inclusions_database.generate_inclusions_database(
      COMPLEX_TEST_CONFIG)

    self.assertIn("timestamp (UTC)", output_db)
    self.assertIn("repo_rev", output_db)
    self.assertIn("config", output_db)
    self.assertEqual(output_db["config"], COMPLEX_TEST_CONFIG)
    verify_complex_included_files_to_including_files(
        self, output_db["included_files_to_including_files"])
    verify_complex_including_files_to_included_files(
        self, output_db["including_files_to_included_files"])
