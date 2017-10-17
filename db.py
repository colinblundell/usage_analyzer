# Definition of configuration and database dictionaries and facilities to
# operate on them (move them to/from disk, generate databases, ...).

import ast
import datetime
import os
import pprint
import subprocess
import sys

# A configuration is of the following form:
CONFIG_TEMPLATE = {
  # A short-but-descriptive name for this config.
  "name" : "descriptive_name",
  # The path to the repository to be analyzed. Can be a relative path, in which
  # case the location is treated as being relative to the location of config.py.
  "repo_root" : "path/to/repo",
  # A list of files whose inclusions are analyzed. Paths should be given
  # relative to |repo_root|.
  "included_files" : ["included/file/1", "included/file/2"],
}

# A database is of the following form:
DATABASE_TEMPLATE = {
  # The configuration that was used to generate this database.
  "config" : {},
  # Map from included files to including files.
  "included_files_to_including_files" : {},
  # Map from including files to included files.
  "including_files_to_included_files" : {},
  # The revision of the repo that was analyzed (i.e., the repo
  # specified by the configuration's |repo_root| field).
  "repo_rev" : "short-rev",
  # The time at which this database was generated.
  "timestamp (UTC)": "timestamp",
}

def validate_config(config):
  assert "name" in config
  assert type(config["name"]) == str
  assert "repo_root" in config
  assert type(config["repo_root"]) == str
  assert "included_files" in config
  assert type(config["included_files"]) == list

# Reads a config from |config_filename| and returns it. Converts |repo_root|
# from a relative to an absolute path following the rule above.
def read_config_from_file(config_filename):
  with open(config_filename, 'r') as config_file:
    config = ast.literal_eval(config_file.read())
  validate_config(config)
  config["repo_root"] = os.path.abspath(config["repo_root"])
  return config

# Generates an output database from the given config and analyses.
def generate_output_database(config, included_files_to_including_files,
                             including_files_to_included_files):
  output_db = {}
  output_db["config"] = config

  now = datetime.datetime.utcnow()
  output_db["timestamp (UTC)"] = str(now)

  repo_rev = subprocess.Popen("git rev-parse --short HEAD",
                              shell=True, stdout=subprocess.PIPE,
                              cwd=config["repo_root"]).stdout.read()
  output_db["repo_rev"] = repo_rev.strip()

  output_db["included_files_to_including_files"] = (
    included_files_to_including_files)
  output_db["including_files_to_included_files"] = (
    including_files_to_included_files)
  return output_db

# Writes the given output database to disk at the following location:
# ./data/output/<config_name>/<repo_rev>/<config_name>_<repo_rev>_inclusions_db.py.
# Warns the user if the above directory already exists.
def write_output_db_to_disk(output_db):
  config_name = output_db["config"]["name"]
  repo_rev = output_db["repo_rev"]
  base_path = "data/output"
  dirname = os.path.join(base_path, config_name, repo_rev)

  if os.path.exists(dirname):
    print "Warning: data already exists for this analysis, risk of overwriting!"
    answer = raw_input("Continue? (y/n)")
    if answer == "n":
      print "Exiting"
      sys.exit(0)
  else:
    os.makedirs(dirname)

  printer = pprint.PrettyPrinter(indent=2)
  database_contents = printer.pformat(output_db)

  database_name = "_".join([config_name, repo_rev, "inclusions_db.py"])
  database_filepath = os.path.join(dirname, database_name)
  with open(database_filepath, "w") as database_file:
    database_file.write(database_contents)

# Reads the given database in from disk.
def read_output_db_from_disk(database_filepath):
  with open(database_filepath, "r") as database_file:
    database = ast.literal_eval(database_file.read())
  return database
