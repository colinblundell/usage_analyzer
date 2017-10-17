# Utilities that are reused across multiple tests.

import os
import unittest

BASIC_TEST_CONFIG = {
  "name" : "basic_test",
  "repo_root" : os.path.abspath("./test/data"),
  "included_files" : [
    "foo/foo.h",
  ],
}

COMPLEX_TEST_CONFIG = {
  "name" : "complex_test",
  "repo_root" : os.path.abspath("./test/data"),
  "included_files" : [
    "bar/bar.h",
    "bar/core.h",
  ],
}

def verify_basic_including_files_to_included_files(test_case,
    including_files_to_included_files):
  including_files = including_files_to_included_files.keys()
  including_files.sort()
  test_case.assertEqual(including_files,
                        ["bar/bar.h", "bar/core.h", "foo/foo.cc"])

def verify_basic_included_files_to_including_files(test_case,
    included_files_to_including_files):
  test_case.assertIn("foo/foo.h", included_files_to_including_files)
  inclusions_of_foo = included_files_to_including_files["foo/foo.h"]
  inclusions_of_foo.sort()
  test_case.assertEqual(inclusions_of_foo,
                        ["bar/bar.h", "bar/core.h", "foo/foo.cc"])

def verify_complex_including_files_to_included_files(test_case,
    including_files_to_included_files):
  including_files = including_files_to_included_files.keys()
  including_files.sort()
  test_case.assertEqual(including_files, ["bar/bar.h",
                                          "bar/baz/bar_core_factory.h",
                                          "foo/foo.h"])

def verify_complex_included_files_to_including_files(test_case,
    included_files_to_including_files):
  test_case.assertIn("bar/bar.h", included_files_to_including_files)
  inclusions_of_bar = included_files_to_including_files["bar/bar.h"]
  inclusions_of_bar.sort()
  test_case.assertEqual(inclusions_of_bar, ["foo/foo.h"])

  test_case.assertIn("bar/core.h", included_files_to_including_files)
  inclusions_of_core = included_files_to_including_files["bar/core.h"]
  inclusions_of_core.sort()
  test_case.assertEqual(inclusions_of_core, ["bar/bar.h",
                                             "bar/baz/bar_core_factory.h"])

