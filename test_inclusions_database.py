import os
import unittest

import git_utils
import inclusions_database
import test_utils


class TestInclusionsDatabase(unittest.TestCase):

  def test_GenerateInclusionsDatabaseSimple(self):
    output_db = inclusions_database.GenerateInclusionsDatabase(
        test_utils.BASIC_TEST_CONFIG)

    self.assertIn("timestamp (UTC)", output_db)
    self.assertIn("repo_rev", output_db)
    self.assertEqual(output_db["repo_rev"],
                     git_utils.GetUsageAnalyzerRepoRevision())
    self.assertIn("usage_analyzer_rev", output_db)
    self.assertEqual(output_db["usage_analyzer_rev"],
                     git_utils.GetUsageAnalyzerRepoRevision())
    self.assertIn("config", output_db)
    self.assertEqual(output_db["config"], test_utils.BASIC_TEST_CONFIG)
    test_utils.VerifyBasicIncludedToIncluding(
        self, output_db["included_to_including"])
    test_utils.VerifyBasicIncludingToIncluded(
        self, output_db["including_to_included"])

  def test_GenerateInclusionsDatabaseComplex(self):
    output_db = inclusions_database.GenerateInclusionsDatabase(
        test_utils.COMPLEX_TEST_CONFIG)

    self.assertIn("timestamp (UTC)", output_db)
    self.assertIn("repo_rev", output_db)
    self.assertEqual(output_db["repo_rev"],
                     git_utils.GetUsageAnalyzerRepoRevision())
    self.assertIn("usage_analyzer_rev", output_db)
    self.assertEqual(output_db["usage_analyzer_rev"],
                     git_utils.GetUsageAnalyzerRepoRevision())
    self.assertIn("config", output_db)
    self.assertEqual(output_db["config"], test_utils.COMPLEX_TEST_CONFIG)
    test_utils.VerifyComplexIncludedToIncluding(
        self, output_db["included_to_including"])
    test_utils.VerifyComplexIncludingToIncluded(
        self, output_db["including_to_included"])

  def test_FilterOutIncludedFilesAsKeysSimple(self):
    db = inclusions_database.GenerateInclusionsDatabase(
        test_utils.BASIC_TEST_CONFIG)

    output = inclusions_database.FilterOutIncludedFilesAsKeys(db)
    expected_output = {"bar/bar.h": ["foo/foo.h"], "bar/core.h": ["foo/foo.h"]}
    self.assertEqual(expected_output, output)

  def test_FilterOutIncludedFilesAsKeysComplex(self):
    db = inclusions_database.GenerateInclusionsDatabase(
        test_utils.COMPLEX_TEST_CONFIG)

    output = inclusions_database.FilterOutIncludedFilesAsKeys(db)
    expected_output = {
        "bar/baz/bar_core_factory.h": ["bar/core.h"],
        "foo/foo.h": ["bar/bar.h"]
    }
    self.assertEqual(expected_output, output)

  def test_FilterOutIncludedFilesAsValuesSimple(self):
    db = inclusions_database.GenerateInclusionsDatabase(
        test_utils.BASIC_TEST_CONFIG)

    output = inclusions_database.FilterOutIncludedFilesAsValues(db)
    expected_output = {"foo/foo.h": ["bar/bar.h", "bar/core.h"]}
    self.assertEqual(expected_output, output)

  def test_FilterOutIncludedFilesAsValuesComplex(self):
    db = inclusions_database.GenerateInclusionsDatabase(
        test_utils.COMPLEX_TEST_CONFIG)

    output = inclusions_database.FilterOutIncludedFilesAsValues(db)
    expected_output = {
        "bar/bar.h": ["foo/foo.h"],
        "bar/core.h": ["bar/baz/bar_core_factory.h"]
    }

    self.assertEqual(expected_output, output)
