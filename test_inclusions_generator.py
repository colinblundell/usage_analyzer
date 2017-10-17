import os
import unittest

import inclusions_generator

TEST_CONFIG = {
  "repo_root" : os.path.abspath("./test/data"),
  "included_files" : [
    "foo/foo.h",
  ],
}

class TestInclusionsGenerator(unittest.TestCase):
  
  def test_map_including_files_to_included_files(self):
    generator = inclusions_generator.InclusionsGenerator(TEST_CONFIG)
    inclusions = generator.map_including_files_to_included_files()
    including_files = inclusions.keys()
    including_files.sort()
    self.assertEqual(including_files, ["bar/bar.h", "bar/core.h", "foo/foo.cc"])

  def test_map_included_files_to_including_files(self):
    generator = inclusions_generator.InclusionsGenerator(TEST_CONFIG)
    inclusions = generator.map_included_files_to_including_files()
    self.assertIn("foo/foo.h", inclusions)
    inclusions_of_foo = inclusions["foo/foo.h"]
    inclusions_of_foo.sort()
    self.assertEqual(inclusions_of_foo, ["bar/bar.h", "bar/core.h", "foo/foo.cc"])
