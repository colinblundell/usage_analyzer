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
  
  def test_find_including_files(self):
    inclusions = inclusions_generator.find_including_files(TEST_CONFIG)
    including_files = inclusions.keys()
    including_files.sort()
    self.assertEqual(including_files, ["bar/bar.h", "bar/core.h", "foo/foo.cc"])
