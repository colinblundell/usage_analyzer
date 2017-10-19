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
