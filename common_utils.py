import copy
import csv
import contextlib
import io
import os
import shutil
import re
import tempfile

# Returns a freshly-created directory that gets automatically deleted after
# usage.
@contextlib.contextmanager
def TemporaryDirectory(suffix='', prefix='tmp'):
  name = tempfile.mkdtemp(suffix=suffix, prefix=prefix)
  try:
    yield name
  finally:
    shutil.rmtree(name)

# Takes in a string and returns a string specifying a regular expression that
# matches the input string's root with any extension.
def root_regex(filepath):
  root = os.path.splitext(filepath)[0]
  output = root + r"\..*"
  return output

# Returns a string that represents |dictionary| in CSV form. |field_names| is
# written as the header, followed by rows of key->value maps in the order
# given by |key_order|.
def dict_to_csv(dictionary, field_names, key_order):
  output = io.BytesIO()

  csv_writer = csv.writer(output)
  csv_writer.writerow(field_names)

  for key in key_order:
    row = [key, dictionary[key]]
    csv_writer.writerow(row)

  return output.getvalue()

# Returns a string that represents |dictionaries| in CSV form. Each dictionary
# in |dictionaries| must be indexed by the set of keys in |key_order|.
# |field_names| is written as the header, followed by rows of
# [key, value1, value2, value3, ...] lines in the order given by |key_order|.
def dicts_to_csv(dictionaries, field_names, key_order):
  output = io.BytesIO()

 
  csv_writer = csv.writer(output)
  csv_writer.writerow(field_names)

  for key in key_order:
    row = [key]
    for dictionary in dictionaries:
      row.append(dictionary[key])
    csv_writer.writerow(row)

  return output.getvalue()


# Takes in a dictionary, a list of keys, and a default value.
# Returns a dictionary that's equivalent to the original but with all
# missing keys filled with the default value.
def dict_with_missing_entries_filled(dictionary, keys, default_value):
  output = copy.deepcopy(dictionary)
  for key in keys:
    if key in output:
      continue
    output[key] = default_value
  return output

# Takes in a list of dictionaries, a list of keys, and a default value.
# Returns a list of dictionaries that's equivalent to the original but with all
# missing keys filled with the default value.
def dicts_with_missing_entries_filled(dictionaries, keys, default_value):
  output = []
  for d in dictionaries:
    output.append(
      dict_with_missing_entries_filled(d, keys, default_value))
  return output

# Takes in a dictionary whose values are lists and returns a dictionary whose
# values are the lengths of the source lists.
def dict_list_values_to_sums(dictionary):
  output_dict = {}
  for key, value in dictionary.items():
    output_dict[key] = len(value)
  return output_dict

# Takes in a dictionary whose values are numbers and returns a list of its keys 
# sorted in order of descending value.
def dict_keys_sorted_by_value(dictionary):
  output_dict = sorted(dictionary, key=lambda k: dictionary[k], reverse=True)
  return output_dict

# Takes in a dictionary whose values are numbers and returns a dictionary that 
# is the input augmented with a "total" key whose value is the sum of all the 
# values.
def dict_with_total(dictionary):
  output_dict = copy.deepcopy(dictionary)
  output_dict["total"] = sum(output_dict.values())
  return output_dict

# Takes in a dictionary whose keys are strings. Returns a dictionary that is 
# equivalent to the original except that keys matching any regex in 
# |regex_list| have been removed.
def dict_filter_keys_matching_regex(dictionary, regex_list):
  output_dict = {}
  patterns = [re.compile(regex) for regex in regex_list]

  for key in dictionary.keys():
    preserve = True

    for pattern in patterns:
      if pattern.match(key):
        preserve = False
        break

    if preserve:
      output_dict[key] = dictionary[key]

  return output_dict

# Takes in a dictionary whose keys are strings and a function that goes from
# string -> string. Returns a dictionary whose keys are outputs of the partition
# function and whose values are the lists of keys from |dictionary| that the
# partition function mapped to that output.
def dict_partition_keys(dictionary, key_partition_function):
  output_dict = {}

  for key in dictionary.keys():
    partition = key_partition_function(key)
    if partition not in output_dict:
      output_dict[partition] = []
    output_dict[partition].append(key)

  return output_dict
