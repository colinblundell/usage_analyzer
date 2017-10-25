# Utilities that are reused across multiple tests.

import os
import unittest

import inclusions_config

BASIC_TEST_CONFIG = {
    "name": "basic_test",
    "repo_root": os.path.abspath("./test/test_repo"),
    "included_files": ["foo/foo.h",],
}
inclusions_config.EvaluateConfig(BASIC_TEST_CONFIG)

COMPLEX_TEST_CONFIG = {
    "name": "complex_test",
    "repo_root": os.path.abspath("./test/test_repo"),
    "included_files": [
        "bar/bar.h",
        "bar/core.h",
    ],
}
inclusions_config.EvaluateConfig(COMPLEX_TEST_CONFIG)


def VerifyBasicIncludingToIncluded(test_case, including_to_included):
  including_files = including_to_included.keys()
  including_files.sort()
  test_case.assertEqual(
      including_files,
      ["bar/bar.h", "bar/core.h", "foo/foo.cc", "foo/foo_unittest.cc"])


def VerifyBasicIncludedToIncluding(test_case, included_to_including):
  test_case.assertIn("foo/foo.h", included_to_including)
  inclusions_of_foo = included_to_including["foo/foo.h"]
  inclusions_of_foo.sort()
  test_case.assertEqual(
      inclusions_of_foo,
      ["bar/bar.h", "bar/core.h", "foo/foo.cc", "foo/foo_unittest.cc"])


def VerifyComplexIncludingToIncluded(test_case, including_to_included):
  including_files = including_to_included.keys()
  including_files.sort()
  test_case.assertEqual(
      including_files, ["bar/bar.h", "bar/baz/bar_core_factory.h", "foo/foo.h"])


def VerifyComplexIncludedToIncluding(test_case, included_to_including):
  test_case.assertIn("bar/bar.h", included_to_including)
  inclusions_of_bar = included_to_including["bar/bar.h"]
  inclusions_of_bar.sort()
  test_case.assertEqual(inclusions_of_bar, ["foo/foo.h"])

  test_case.assertIn("bar/core.h", included_to_including)
  inclusions_of_core = included_to_including["bar/core.h"]
  inclusions_of_core.sort()
  test_case.assertEqual(inclusions_of_core,
                        ["bar/bar.h", "bar/baz/bar_core_factory.h"])
