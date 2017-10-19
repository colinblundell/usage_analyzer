import os
import unittest

import common_utils

class TestCommonUtils(unittest.TestCase):
  def test_dict_to_csv(self):
    test_dict = {"key1" : "val1", "key2" : "val2", "key3" : "val3"}
    field_names = ["name", "value"]
    key_order = ["key3", "key1", "key2"]
  
    expected_output = "name,value\r\nkey3,val3\r\nkey1,val1\r\nkey2,val2\r\n"
    output = common_utils.dict_to_csv(test_dict, field_names, key_order)
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

