import os
import unittest

import inclusions_generator
import test_utils


class TestInclusionsGenerator(unittest.TestCase):

  def test_map_including_to_included_basic(self):
    generator = inclusions_generator.InclusionsGenerator(
        test_utils.BASIC_TEST_CONFIG)
    inclusions = generator.map_including_to_included()
    test_utils.verify_basic_including_to_included(self, inclusions)

  def test_map_included_to_including_basic(self):
    generator = inclusions_generator.InclusionsGenerator(
        test_utils.BASIC_TEST_CONFIG)
    inclusions = generator.map_included_to_including()
    test_utils.verify_basic_included_to_including(self, inclusions)

  def test_map_including_to_included_complex(self):
    generator = inclusions_generator.InclusionsGenerator(
        test_utils.COMPLEX_TEST_CONFIG)
    inclusions = generator.map_including_to_included()
    test_utils.verify_complex_including_to_included(self, inclusions)

  def test_map_included_to_including_complex(self):
    generator = inclusions_generator.InclusionsGenerator(
        test_utils.COMPLEX_TEST_CONFIG)
    inclusions = generator.map_included_to_including()
    test_utils.verify_complex_included_to_including(self, inclusions)
