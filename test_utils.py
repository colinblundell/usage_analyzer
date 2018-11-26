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

BASIC_TEST_INCLUDED_FILES_TO_LIMIT_TO = ["foo/foo.h"]

COMPLEX_TEST_CONFIG = {
    "name": "complex_test",
    "repo_root": os.path.abspath("./test/test_repo"),
    "included_files": [
        "bar/bar.h",
        "bar/core.h",
    ],
}
inclusions_config.EvaluateConfig(COMPLEX_TEST_CONFIG)

COMPLEX_TEST_INCLUDED_FILES_TO_LIMIT_TO = ["bar/bar.h"]


def VerifyBasicIncludingToIncluded(test_case, including_to_included):
  including_files = including_to_included.keys()
  including_files.sort()

  expected_including_files = [
      "bar/bar.h", "bar/core.h", "foo/foo.cc", "foo/foo_unittest.cc"
  ]
  test_case.assertEqual(including_files, expected_including_files)

  for f in including_to_included:
    test_case.assertEqual(including_to_included[f], ["foo/foo.h"])


def VerifyBasicIncludingToIncludedWithLimitedIncludes(test_case,
                                                      including_to_included):
  # Nothing should have changed, as the set to limit to is equal to the original
  # |included_files| set.
  VerifyBasicIncludingToIncluded(test_case, including_to_included)


def VerifyBasicIncludedToIncluding(test_case, included_to_including):
  test_case.assertIn("foo/foo.h", included_to_including)
  inclusions_of_foo = included_to_including["foo/foo.h"]
  inclusions_of_foo.sort()
  test_case.assertEqual(
      inclusions_of_foo,
      ["bar/bar.h", "bar/core.h", "foo/foo.cc", "foo/foo_unittest.cc"])


def VerifyBasicIncludedToIncludingWithLimitedIncludes(test_case,
                                                      included_to_including):
  # Nothing should have changed, as the set to limit to is equal to the original
  # |included_files| set.
  VerifyBasicIncludedToIncluding(test_case, including_to_included)


def VerifyComplexIncludingToIncluded(test_case, including_to_included):
  including_files = including_to_included.keys()
  including_files.sort()
  test_case.assertEqual(
      including_files, ["bar/bar.h", "bar/baz/bar_core_factory.h", "foo/foo.h"])
  test_case.assertEqual(including_to_included["bar/bar.h"], ["bar/core.h"])
  test_case.assertEqual(including_to_included["bar/baz/bar_core_factory.h"],
                        ["bar/core.h"])
  test_case.assertEqual(including_to_included["foo/foo.h"],
                        ["bar/bar.h", "bar/core.h"])


def VerifyComplexIncludedToIncluding(test_case, included_to_including):
  test_case.assertIn("bar/bar.h", included_to_including)
  inclusions_of_bar = included_to_including["bar/bar.h"]
  inclusions_of_bar.sort()
  test_case.assertEqual(inclusions_of_bar, ["foo/foo.h"])

  test_case.assertIn("bar/core.h", included_to_including)
  inclusions_of_core = included_to_including["bar/core.h"]
  inclusions_of_core.sort()
  test_case.assertEqual(
      inclusions_of_core,
      ["bar/bar.h", "bar/baz/bar_core_factory.h", "foo/foo.h"])
