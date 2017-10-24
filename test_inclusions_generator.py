import os
import unittest

import inclusions_generator
import test_utils


class TestInclusionsGenerator(unittest.TestCase):

  def test_MapIncludingToIncludedBasic(self):
    generator = inclusions_generator.InclusionsGenerator(
        test_utils.BASIC_TEST_CONFIG)
    inclusions = generator.MapIncludingToIncluded()
    test_utils.VerifyBasicIncludingToIncluded(self, inclusions)

  def test_MapIncludedToIncludingBasic(self):
    generator = inclusions_generator.InclusionsGenerator(
        test_utils.BASIC_TEST_CONFIG)
    inclusions = generator.MapIncludedToIncluding()
    test_utils.VerifyBasicIncludedToIncluding(self, inclusions)

  def test_MapIncludingToIncludedComplex(self):
    generator = inclusions_generator.InclusionsGenerator(
        test_utils.COMPLEX_TEST_CONFIG)
    inclusions = generator.MapIncludingToIncluded()
    test_utils.VerifyComplexIncludingToIncluded(self, inclusions)

  def test_MapIncludedToIncludingComplex(self):
    generator = inclusions_generator.InclusionsGenerator(
        test_utils.COMPLEX_TEST_CONFIG)
    inclusions = generator.MapIncludedToIncluding()
    test_utils.VerifyComplexIncludedToIncluding(self, inclusions)
