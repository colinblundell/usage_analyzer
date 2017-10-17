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
  
  def test_generate_inclusions(self):
    inclusions = inclusions_generator.generateInclusionsForConfig(TEST_CONFIG)
    including_files = inclusions.keys()
    including_files.sort()
    self.assertEqual(including_files, ["bar/bar.h", "bar/core.h", "foo/foo.cc"])
