# Definition of configuration and database dictionaries and facilities to 
# operate on them (move them to/from disk, generate databases, ...).

import ast
import datetime
import os
import pprint
import subprocess

# A configuration is of the following form:
CONFIG_TEMPLATE = {
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

def write_output_db_to_file(output_db, output_path):
  print output_path
  print
  printer = pprint.PrettyPrinter(indent=2)
  printer.pprint(output_db)
