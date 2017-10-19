# Definition of inclusions database dictionaries and facilities to
# operate on them (move them to/from disk, generate databases, ...).

import ast
import datetime
import os
import pprint
import sys

import common_utils
import git_utils
import inclusions_config
import inclusions_generator

# A database is of the following form:
DATABASE_TEMPLATE = {
  # The configuration that was used to generate this database.
  "config" : {},
  # Map from included files to including files.
  "included_files_to_including_files" : {},
  # Map from including files to included files.
  "including_files_to_included_files" : {},
  # The revision of the repo that was analyzed (i.e., the repo
  # specified by the configuration's |evaluated_repo_root| field).
  "repo_rev" : "short-rev",
  # The time at which this database was generated.
  "timestamp (UTC)": "timestamp",
}

# Generates an inclusions database from the given inclusions config.
def generate_inclusions_database(config):
  generator = inclusions_generator.InclusionsGenerator(config)
  including_files_to_included_files = (
    generator.map_including_files_to_included_files())
  included_files_to_including_files = (
    generator.map_included_files_to_including_files())

  inclusions_db = {}
  inclusions_db["config"] = config

  now = datetime.datetime.utcnow()
  inclusions_db["timestamp (UTC)"] = str(now)

  repo_rev = git_utils.get_repo_revision(config["evaluated_repo_root"])
  inclusions_db["repo_rev"] = repo_rev

  usage_analyzer_rev = git_utils.get_usage_analyzer_repo_revision()
  inclusions_db["usage_analyzer_rev"] = usage_analyzer_rev

  inclusions_db["included_files_to_including_files"] = (
    included_files_to_including_files)
  inclusions_db["including_files_to_included_files"] = (
    including_files_to_included_files)

  return inclusions_db

# Writes the given output database to disk at the following location:
# <output_dir>/<config_name>/<repo_rev>/<config_name>_<repo_rev>_inclusions_db.py.
# Warns the user if the above directory already exists.
def write_inclusions_db_to_disk(inclusions_db, output_dir):
  config_name = inclusions_db["config"]["name"]
  repo_rev = inclusions_db["repo_rev"]
  dirname = os.path.join(output_dir, config_name, repo_rev)

  if os.path.exists(dirname):
    print "Warning: data already exists for this analysis, risk of overwriting!"
    answer = raw_input("Continue? (y/n)")
    if answer == "n":
      print "Exiting"
      sys.exit(0)
  else:
    os.makedirs(dirname)

  printer = pprint.PrettyPrinter(indent=2)
  database_contents = printer.pformat(inclusions_db)

  database_name = "_".join([config_name, repo_rev, "inclusions_db.py"])
  database_filepath = os.path.join(dirname, database_name)
  with open(database_filepath, "w") as database_file:
    database_file.write(database_contents)
    database_file.write("\n")

# Reads the given database in from disk.
def read_inclusions_db_from_disk(database_filepath):
  with open(database_filepath, "r") as database_file:
    database = ast.literal_eval(database_file.read())
  return database

# Takes in an inclusions database and returns
# an including_files_to_included_files dictionary that has no included files as
# keys.
def filter_including_files_by_included_files(inclusions_db):
  included_files = inclusions_db["config"]["included_files"]
  included_files_regexes = [
    common_utils.root_regex(f) for f in included_files]

  output_dict = common_utils.dict_filter_keys_matching_regex(
    inclusions_db["including_files_to_included_files"],
    included_files_regexes)

  return output_dict
