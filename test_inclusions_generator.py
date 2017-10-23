import os
import unittest

import inclusions_generator
from test_utils import *


class TestInclusionsGenerator(unittest.TestCase):

  def test_map_including_to_included_basic(self):
    generator = inclusions_generator.InclusionsGenerator(BASIC_TEST_CONFIG)
    inclusions = generator.map_including_to_included()
    verify_basic_including_to_included(self, inclusions)

  def test_map_included_to_including_basic(self):
    generator = inclusions_generator.InclusionsGenerator(BASIC_TEST_CONFIG)
    inclusions = generator.map_included_to_including()
    verify_basic_included_to_including(self, inclusions)

  def test_map_including_to_included_complex(self):
    generator = inclusions_generator.InclusionsGenerator(COMPLEX_TEST_CONFIG)
    inclusions = generator.map_including_to_included()
    verify_complex_including_to_included(self, inclusions)

  def test_map_included_to_including_complex(self):
    generator = inclusions_generator.InclusionsGenerator(COMPLEX_TEST_CONFIG)
    inclusions = generator.map_included_to_including()
    verify_complex_included_to_including(self, inclusions)
