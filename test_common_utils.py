import os
import unittest

import common_utils

class TestCommonUtils(unittest.TestCase):
  def test_root_regex(self):
    test_filepath = "foo/bar.h"
    expected_output = r"foo/bar\..*"
    output = common_utils.root_regex(test_filepath)
    self.assertEqual(expected_output, output)

  def test_dict_to_csv(self):
    test_dict = {"key1" : "val1", "key2" : "val2", "key3" : "val3"}
    field_names = ["name", "value"]
    key_order = ["key3", "key1", "key2"]
  
    expected_output = "name,value\r\nkey3,val3\r\nkey1,val1\r\nkey2,val2\r\n"
    output = common_utils.dict_to_csv(test_dict, field_names, key_order)
    self.assertEqual(expected_output, output)

  def test_dicts_to_csv(self):
    test_dict_a = {"key1" : "vala1", "key2" : "vala2", "key3" : "vala3"}
    test_dict_b = {"key1" : "valb1", "key2" : "valb2", "key3" : "valb3"}
    test_dict_c = {"key1" : "valc1", "key2" : "valc2", "key3" : "valc3"}
    test_dicts = [test_dict_c, test_dict_a, test_dict_b]
    field_names = ["name", "value"]
    key_order = ["key3", "key1", "key2"]
  
    expected_output = "name,value\r\nkey3,valc3,vala3,valb3\r\nkey1,valc1,vala1,valb1\r\nkey2,valc2,vala2,valb2\r\n"
    output = common_utils.dicts_to_csv(test_dicts, field_names, key_order)
    self.assertEqual(expected_output, output)

  def test_dict_list_values_to_sums(self):
    test_dict = {"key1" : [1, 2, 3, 4], "key2" : [], "key3" : [1]}
    expected_output = {"key1" : 4, "key2" : 0, "key3" : 1}
    output = common_utils.dict_list_values_to_sums(test_dict)
    self.assertEqual(expected_output, output)

  def test_dict_keys_sorted_by_value(self):
    test_dict = {"key1" : 2, "key2" : 0, "key3" : 4}
    expected_output = ["key3", "key1", "key2"]
    output = common_utils.dict_keys_sorted_by_value(test_dict)
    self.assertEqual(expected_output, output)

  def test_dict_with_total(self):
    test_dict = {"key1" : 2, "key2" : 0, "key3" : 4}
    expected_output = {"key1" : 2, "key2" : 0, "key3" : 4, "total" : 6}
    output = common_utils.dict_with_total(test_dict)
    self.assertEqual(expected_output, output)

  def test_dict_filter_keys_matching_regex(self):
    test_dict = {"foo.h" : ["bar.h"],
                 "foo.cc" : ["foo.h", "bar.h"],
                 "bar.h" : ["baz.h", "qux.h"],
                 "bad/bad.h" : ["baz.h", "foo.h"]}
    test_regexes = [r"foo\..*", r"bad/.*"]
    expected_output = {"bar.h" : ["baz.h", "qux.h"]}
    output = common_utils.dict_filter_keys_matching_regex(test_dict,
                                                          test_regexes)
    self.assertEqual(expected_output, output)

  def test_dict_partition_keys(self):
    test_dict = {"foo.h" : ["bar.h"],
                 "foo.cc" : ["foo.h", "bar.h"],
                 "bar.h" : ["baz.h", "qux.h"],
                 "bad/bad.h" : ["baz.h", "foo.h"]}
    def test_partition_function(key):
      if key.startswith("foo"):
        return "foo"
      if key.startswith("bar"):
        return "bar"
      if key.startswith("bad"):
        return "bad"
      return None

    # TODO: This makes an assumption on list ordering and so is somewhat
    # fragile.
    expected_output = {"foo" : ["foo.cc", "foo.h"],
                       "bar" : ["bar.h"],
                       "bad" : ["bad/bad.h"]}
    output = common_utils.dict_partition_keys(test_dict, 
                                              test_partition_function)
    self.assertEqual(expected_output, output)
