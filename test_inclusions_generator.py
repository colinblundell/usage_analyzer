import os
import unittest

import inclusions_generator
from test_utils import *


class TestInclusionsGenerator(unittest.TestCase):

  def test_map_including_files_to_included_files_basic(self):
    generator = inclusions_generator.InclusionsGenerator(BASIC_TEST_CONFIG)
    inclusions = generator.map_including_files_to_included_files()
    verify_basic_including_files_to_included_files(self, inclusions)

  def test_map_included_files_to_including_files_basic(self):
    generator = inclusions_generator.InclusionsGenerator(BASIC_TEST_CONFIG)
    inclusions = generator.map_included_files_to_including_files()
    verify_basic_included_files_to_including_files(self, inclusions)

  def test_map_including_files_to_included_files_complex(self):
    generator = inclusions_generator.InclusionsGenerator(COMPLEX_TEST_CONFIG)
    inclusions = generator.map_including_files_to_included_files()
    verify_complex_including_files_to_included_files(self, inclusions)

  def test_map_included_files_to_including_files_complex(self):
    generator = inclusions_generator.InclusionsGenerator(COMPLEX_TEST_CONFIG)
    inclusions = generator.map_included_files_to_including_files()
    verify_complex_included_files_to_including_files(self, inclusions)
