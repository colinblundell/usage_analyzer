# Definition of configurations for generating inclusions and facilities to
# operate on them.

import ast
import os

# A configuration is of the following form:
CONFIG_TEMPLATE = {
  # A short-but-descriptive name for this config.
  "name" : "descriptive_name",
  # The path to the repository to be analyzed. Can be a relative path, in which
  # case the location is evaluated as being relative to the location of
  # config.py.  Can also be "CHROMIUM_ROOT", in which case the "chromium_root"
  # key below is added as the evaluated root.
  "repo_root" : "path/to/repo",
  # Added during evaluation of the config, based on evaluation of the
  # |repo_root| field as specified above.
  "evaluated_repo_root" : "/abs/path/to/repo",
  # A list of files whose inclusions are analyzed. Paths should be given
  # relative to |repo_root|.
  "included_files" : ["included/file/1", "included/file/2"],
}

# Validates a config's format and the fact that it has been evaluated.
def validate_config(config):
  assert "name" in config
  assert type(config["name"]) == str
  assert "repo_root" in config
  assert type(config["repo_root"]) == str
  assert "evaluated_repo_root" in config
  assert type(config["evaluated_repo_root"]) == str
  assert "included_files" in config
  assert type(config["included_files"]) == list

# Evaluates |config| in-place, following the evaluation rules mentioned above.
def evaluate_config(config, chromium_root=""):
  if (config["repo_root"] == "CHROMIUM_ROOT"):
    assert chromium_root != ""
    config["evaluated_repo_root"] = chromium_root
  else:
    config["evaluated_repo_root"] = os.path.abspath(config["repo_root"])

# Evaluates a config from |config_filename| and returns it. 
def read_config_from_file(config_filename, chromium_root):
  with open(config_filename, 'r') as config_file:
    config = ast.literal_eval(config_file.read())
  evaluate_config(config, chromium_root)
  validate_config(config)
  return config
