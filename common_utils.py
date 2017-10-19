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
