import os
import unittest

import inclusions_generator

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

class TestInclusionsGenerator(unittest.TestCase):

  def verify_basic_including_files_to_included_files(self,
      including_files_to_included_files):
    including_files = including_files_to_included_files.keys()
    including_files.sort()
    self.assertEqual(including_files, ["bar/bar.h", "bar/core.h", "foo/foo.cc"])

  def verify_basic_included_files_to_including_files(self,
      included_files_to_including_files):
    self.assertIn("foo/foo.h", included_files_to_including_files)
    inclusions_of_foo = included_files_to_including_files["foo/foo.h"]
    inclusions_of_foo.sort()
    self.assertEqual(inclusions_of_foo, ["bar/bar.h", "bar/core.h",
                                         "foo/foo.cc"])

  def verify_complex_including_files_to_included_files(self,
      including_files_to_included_files):
    including_files = including_files_to_included_files.keys()
    including_files.sort()
    self.assertEqual(including_files, ["bar/bar.h",
                                       "bar/baz/bar_core_factory.h",
                                       "foo/foo.h"])

  def verify_complex_included_files_to_including_files(self,
      included_files_to_including_files):
    self.assertIn("bar/bar.h", included_files_to_including_files)
    inclusions_of_bar = included_files_to_including_files["bar/bar.h"]
    inclusions_of_bar.sort()
    self.assertEqual(inclusions_of_bar, ["foo/foo.h"])

    self.assertIn("bar/core.h", included_files_to_including_files)
    inclusions_of_core = included_files_to_including_files["bar/core.h"]
    inclusions_of_core.sort()
    self.assertEqual(inclusions_of_core, ["bar/bar.h",
                                          "bar/baz/bar_core_factory.h"])

  def test_map_including_files_to_included_files_basic(self):
    generator = inclusions_generator.InclusionsGenerator(BASIC_TEST_CONFIG)
    inclusions = generator.map_including_files_to_included_files()
    self.verify_basic_including_files_to_included_files(inclusions)

  def test_map_included_files_to_including_files_basic(self):
    generator = inclusions_generator.InclusionsGenerator(BASIC_TEST_CONFIG)
    inclusions = generator.map_included_files_to_including_files()
    self.verify_basic_included_files_to_including_files(inclusions)

  def test_map_including_files_to_included_files_complex(self):
    generator = inclusions_generator.InclusionsGenerator(COMPLEX_TEST_CONFIG)
    inclusions = generator.map_including_files_to_included_files()
    self.verify_complex_including_files_to_included_files(inclusions)

  def test_map_included_files_to_including_files_complex(self):
    generator = inclusions_generator.InclusionsGenerator(COMPLEX_TEST_CONFIG)
    inclusions = generator.map_included_files_to_including_files()
    self.verify_complex_included_files_to_including_files(inclusions)
