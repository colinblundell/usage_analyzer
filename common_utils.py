import csv
import contextlib
import io
import shutil
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
  output_dict = {}
  for key, value in dictionary.items():
    output_dict[key] = value
  output_dict["total"] = sum(output_dict.values())
  return output_dict
