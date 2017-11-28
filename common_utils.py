import ast
import copy
import csv
import contextlib
import io
import os
import shutil
import re
import tempfile

# TODO: Rename these? They're confusing because they're a little backwards, but
# the way they're used in other files then becomes confusing if they're named
# the other way.

# Regexes that filter out test files, leaving only prod files.
PROD_FILTERS = [".*fake.*", ".*test.*"]

# Regexes that filter factories.
NON_FACTORY_FILTERS = [".*_factory.*"]

# Regexes that filter both test files and factories.
PROD_NON_FACTORY_FILTERS = PROD_FILTERS + NON_FACTORY_FILTERS


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
def RootRegex(filepath):
  root = os.path.splitext(filepath)[0]
  output = root + r"\..*"
  return output


# Takes in a string and returns a string specifying a regular expression that
# matches the input string's root with a "_unittest" suffix and any extension.
def UnittestRegex(filepath):
  root = os.path.splitext(filepath)[0]
  output = root + r"_unittest\..*"
  return output


# Returns a string that represents |dictionary| in CSV form. |field_names| is
# written as the header, followed by rows of key->value maps in the order
# given by |key_order|.
def DictToCsv(dictionary, field_names, key_order):
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
def DictsToCsv(dictionaries, field_names, key_order):
  output = io.BytesIO()

  csv_writer = csv.writer(output)
  csv_writer.writerow(field_names)

  for key in key_order:
    row = [key]
    for dictionary in dictionaries:
      row.append(dictionary[key])
    csv_writer.writerow(row)

  return output.getvalue()


# Takes in a dictionary and a value.
# Returns a dictionary that's equivalent to the original but with all
# keys that have the given value removed.
# |keys_to_keep| is a list of keys that are preserved even if their value
# matches |value_to_remove|.
def DictWithValueRemoved(dictionary, value_to_remove, keys_to_keep=[]):
  output = {}
  for key, value in dictionary.iteritems():
    if value == value_to_remove and key not in keys_to_keep:
      continue
    output[key] = value
  return output


# Takes in a dictionary, a list of keys, and a default value.
# Returns a dictionary that's equivalent to the original but with all
# missing keys filled with the default value.
def DictWithMissingEntriesFilled(dictionary, keys, default_value):
  output = copy.deepcopy(dictionary)
  for key in keys:
    if key in output:
      continue
    output[key] = default_value
  return output


# Takes in a list of dictionaries, a list of keys, and a default value.
# Returns a list of dictionaries that's equivalent to the original but with all
# missing keys filled with the default value.
def DictsWithMissingEntriesFilled(dictionaries, keys, default_value):
  output = []
  for d in dictionaries:
    output.append(DictWithMissingEntriesFilled(d, keys, default_value))
  return output


# Takes in two dictionaries mapping strings to numbers and returns a dictionary
# representing the difference. Specifically, for a given key k:
# if k is in dict1 and dict2, diff[k] = dict2[k] - dict1[k]
# if k is in dict1 but not dict2, diff[k] = 0 - dict1[k]
# if k is in dict2 but not dict1, diff[k] = dict2[k]
def DifferenceBetweenDicts(dict1, dict2):
  diff_dict = {}

  for k, v in dict2.iteritems():
    diff = v
    if k in dict1:
      diff -= dict1[k]
    diff_dict[k] = diff

  for k in set(dict1.keys()) - set(dict2.keys()):
    diff_dict[k] = -(dict1[k])

  return diff_dict


# Takes in a dictionary whose values are lists and returns a dictionary whose
# values are the lengths of the source lists.
def DictListValuesToSums(dictionary):
  output_dict = {}
  for key, value in dictionary.items():
    output_dict[key] = len(value)
  return output_dict


# Takes in a dictionary whose values are numbers and returns a list of its keys
# sorted in order of descending value.
def DictKeysSortedByValue(dictionary):
  output_dict = sorted(dictionary, key=lambda k: dictionary[k], reverse=True)
  return output_dict


# Takes in a dictionary whose values are numbers and returns a dictionary that
# is the input augmented with a "total" key whose value is the sum of all the
# values.
def DictWithTotal(dictionary):
  output_dict = copy.deepcopy(dictionary)
  output_dict["total"] = sum(output_dict.values())
  return output_dict


# Takes in a dictionary whose keys are strings. Returns a dictionary that is
# equivalent to the original except that keys matching any regex in
# |regex_list| have been removed.
def DictFilterKeysMatchingRegex(dictionary, regex_list):
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


# Takes in a dictionary whose values are list of strings. Returns a dictionary
# that is equivalent to the original except that the values have been pruned
# such that strings matching any regex in |regex_list| have been removed.
def DictFilterValuesMatchingRegex(dictionary, regex_list):
  output_dict = {}
  patterns = [re.compile(regex) for regex in regex_list]

  for key, value_list in dictionary.iteritems():

    output_dict[key] = []
    for value in value_list:
      preserve = True
      for pattern in patterns:
        if pattern.match(value):
          preserve = False
          break

      if preserve:
        output_dict[key].append(value)

  return output_dict


# Takes in a dictionary whose keys are strings and a function that goes from
# string -> string. Returns a dictionary whose keys are outputs of the partition
# function and whose values are the lists of keys from |dictionary| that the
# partition function mapped to that output.
def DictPartitionKeys(dictionary, key_partition_function):
  output_dict = {}

  for key in dictionary.keys():
    partition = key_partition_function(key)
    if partition not in output_dict:
      output_dict[partition] = []
    output_dict[partition].append(key)

  return output_dict


# Returns True if this string matches any of the regexes in |regex_list|.
def MatchesOneOfRegexes(string, regex_list):
  patterns = [re.compile(regex) for regex in regex_list]
  for pattern in patterns:
    if pattern.match(string):
      return True
  return False


# Takes in a list of filenames and returns a list of filenames in the following
# order:
# prod non-factory files
# prod factory files
# test files
# Within each section of the list, files are in the order given in |filenames|.
def FilenamesSeparatedByProdStatus(filenames):
  prod_non_factory_files = []
  prod_factory_files = []
  test_files = []

  for filename in filenames:
    if MatchesOneOfRegexes(filename, PROD_FILTERS):
      test_files.append(filename)
    elif MatchesOneOfRegexes(filename, PROD_NON_FACTORY_FILTERS):
      prod_factory_files.append(filename)
    else:
      prod_non_factory_files.append(filename)

  return prod_non_factory_files + prod_factory_files + test_files


# Takes in a filepath and evaluates its contents as a Python literal.
def EvaluateLiteralFromDisk(filepath):
  with open(filepath, "r") as file_to_eval:
    literal = ast.literal_eval(file_to_eval.read())
  return literal

