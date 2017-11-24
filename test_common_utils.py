import os
import unittest

import common_utils


class TestCommonUtils(unittest.TestCase):

  def test_RootRegex(self):
    test_filepath = "foo/bar.h"
    expected_output = r"foo/bar\..*"
    output = common_utils.RootRegex(test_filepath)
    self.assertEqual(expected_output, output)

  def test_UnittestRegex(self):
    test_filepath = "foo/bar.h"
    expected_output = r"foo/bar_unittest\..*"
    output = common_utils.UnittestRegex(test_filepath)
    self.assertEqual(expected_output, output)

  def test_DictToCsv(self):
    test_dict = {"key1": "val1", "key2": "val2", "key3": "val3"}
    field_names = ["name", "value"]
    key_order = ["key3", "key1", "key2"]

    expected_output = "name,value\r\nkey3,val3\r\nkey1,val1\r\nkey2,val2\r\n"
    output = common_utils.DictToCsv(test_dict, field_names, key_order)
    self.assertEqual(expected_output, output)

  def test_DictsToCsv(self):
    test_dict_a = {"key1": "vala1", "key2": "vala2", "key3": "vala3"}
    test_dict_b = {"key1": "valb1", "key2": "valb2", "key3": "valb3"}
    test_dict_c = {"key1": "valc1", "key2": "valc2", "key3": "valc3"}
    test_dicts = [test_dict_c, test_dict_a, test_dict_b]
    field_names = ["name", "value"]
    key_order = ["key3", "key1", "key2"]

    expected_output = "name,value\r\nkey3,valc3,vala3,valb3\r\n"
    expected_output += "key1,valc1,vala1,valb1\r\n"
    expected_output += "key2,valc2,vala2,valb2\r\n"
    output = common_utils.DictsToCsv(test_dicts, field_names, key_order)
    self.assertEqual(expected_output, output)

  def test_DictWithValueRemoved(self):
    test_dict = {"key2": 5}
    keys = ["key1", "key2", "key3"]
    expected_output = {"key1": 0, "key2": 5, "key3": 0}
    output = common_utils.DictWithMissingEntriesFilled(test_dict, keys, 0)
    self.assertEqual(expected_output, output)

  def test_DictWithMissingEntriesFilled(self):
    test_dict = {"key1": 0, "key2": 5, "key3": -1, "key4": 0, "key5": 5}
    expected_output = {"key2": 5, "key3": -1, "key4": 0, "key5": 5}
    output = common_utils.DictWithValueRemoved(
        test_dict, 0, keys_to_keep=["key4"])
    self.assertEqual(expected_output, output)

  def test_DictsWithMissingEntriesFilled(self):
    test_dict_a = {"key2": 5}
    test_dict_b = {"key1": 3}
    keys = ["key1", "key2", "key3"]
    expected_output = [{
        "key1": 0,
        "key2": 5,
        "key3": 0
    }, {
        "key1": 3,
        "key2": 0,
        "key3": 0
    }]
    output = common_utils.DictsWithMissingEntriesFilled(
        [test_dict_a, test_dict_b], keys, 0)
    self.assertEqual(expected_output, output)

  def test_DifferenceBetweenDicts(self):
    test_dict_1 = {"key1": 2, "key2": 5, "key4": 3}
    test_dict_2 = {"key1": 3, "key3": 8, "key4": 3}
    expected_output = {"key1": 1, "key2": -5, "key3": 8, "key4": 0}
    output = common_utils.DifferenceBetweenDicts(test_dict_1, test_dict_2)
    self.assertEqual(expected_output, output)

  def test_DictListValuesToSums(self):
    test_dict = {"key1": [1, 2, 3, 4], "key2": [], "key3": [1]}
    expected_output = {"key1": 4, "key2": 0, "key3": 1}
    output = common_utils.DictListValuesToSums(test_dict)
    self.assertEqual(expected_output, output)

  def test_DictKeysSortedByValue(self):
    test_dict = {"key1": 2, "key2": 0, "key3": 4}
    expected_output = ["key3", "key1", "key2"]
    output = common_utils.DictKeysSortedByValue(test_dict)
    self.assertEqual(expected_output, output)

  def test_DictWithTotal(self):
    test_dict = {"key1": 2, "key2": 0, "key3": 4}
    expected_output = {"key1": 2, "key2": 0, "key3": 4, "total": 6}
    output = common_utils.DictWithTotal(test_dict)
    self.assertEqual(expected_output, output)

  def test_DictFilterKeysMatchingRegex(self):
    test_dict = {
        "foo.h": ["bar.h"],
        "foo.cc": ["foo.h", "bar.h"],
        "bar.h": ["baz.h", "qux.h"],
        "bad/bad.h": ["baz.h", "foo.h"]
    }
    test_regexes = [r"foo\..*", r"bad/.*"]
    expected_output = {"bar.h": ["baz.h", "qux.h"]}
    output = common_utils.DictFilterKeysMatchingRegex(test_dict, test_regexes)
    self.assertEqual(expected_output, output)

  def test_DictFilterValuesMatchingRegex(self):
    test_dict = {
        "foo.h": ["bar.h", "foo.cc", "baz.h"],
        "bar.h": ["foo.cc", "baz.h", "qux.h"],
    }
    test_regexes = [r"foo\..*", r"bar\..*"]
    expected_output = {"foo.h": ["baz.h"], "bar.h": ["baz.h", "qux.h"]}
    output = common_utils.DictFilterValuesMatchingRegex(test_dict, test_regexes)
    self.assertEqual(expected_output, output)

  def test_DictPartitionKeys(self):
    test_dict = {
        "foo.h": ["bar.h"],
        "foo.cc": ["foo.h", "bar.h"],
        "bar.h": ["baz.h", "qux.h"],
        "bad/bad.h": ["baz.h", "foo.h"]
    }

    def test_PartitionFunction(key):
      if key.startswith("foo"):
        return "foo"
      if key.startswith("bar"):
        return "bar"
      if key.startswith("bad"):
        return "bad"
      return None

    # TODO: This makes an assumption on list ordering and so is somewhat
    # fragile.
    expected_output = {
        "foo": ["foo.cc", "foo.h"],
        "bar": ["bar.h"],
        "bad": ["bad/bad.h"]
    }
    output = common_utils.DictPartitionKeys(test_dict, test_PartitionFunction)
    self.assertEqual(expected_output, output)

  def test_MatchesOneOfRegexes(self):
    test_regexes = ["..*foo", "bar.*"]
    self.assertEqual(
        common_utils.MatchesOneOfRegexes("ab_foo", test_regexes), True)
    self.assertEqual(
        common_utils.MatchesOneOfRegexes("foosh", test_regexes), False)
    self.assertEqual(
        common_utils.MatchesOneOfRegexes("bar", test_regexes), True)
    self.assertEqual(
        common_utils.MatchesOneOfRegexes("morebar", test_regexes), False)

  def test_FilenamesSeparatedByProdStatus(self):
    filenames = [
        "foo_factory.h",
        "bar/bar_unittest.cc",
        "foo.h",
        "baz_unittest.cc",
        "bar/bar.h",
        "bar/bar_factory.cc",
        "baz.cc",
    ]

    expected_output = [
        "foo.h",
        "bar/bar.h",
        "baz.cc",
        "foo_factory.h",
        "bar/bar_factory.cc",
        "bar/bar_unittest.cc",
        "baz_unittest.cc",
    ]

    output = common_utils.FilenamesSeparatedByProdStatus(filenames)
    self.assertEqual(expected_output, output)
