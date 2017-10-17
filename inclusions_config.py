# Definition of configurations for generating inclusions and facilities to
# operate on them.

import ast
import os

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
