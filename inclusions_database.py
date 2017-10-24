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
    "config": {},
    # Map from included files to including files.
    "included_to_including": {},
    # Map from including files to included files.
    "including_to_included": {},
    # The revision of the repo that was analyzed (i.e., the repo
    # specified by the configuration's |evaluated_repo_root| field).
    "repo_rev": "short-rev",
    # The time at which this database was generated.
    "timestamp (UTC)": "timestamp",
}


# Generates an inclusions database from the given inclusions config.
def GenerateInclusionsDatabase(config):
  generator = inclusions_generator.InclusionsGenerator(config)
  including_to_included = (generator.MapIncludingToIncluded())
  included_to_including = (generator.MapIncludedToIncluding())

  inclusions_db = {}
  inclusions_db["config"] = config

  now = datetime.datetime.utcnow()
  inclusions_db["timestamp (UTC)"] = str(now)

  repo_rev = git_utils.GetRepoRevision(config["evaluated_repo_root"])
  inclusions_db["repo_rev"] = repo_rev

  usage_analyzer_rev = git_utils.GetUsageAnalyzerRepoRevision()
  inclusions_db["usage_analyzer_rev"] = usage_analyzer_rev

  inclusions_db["included_to_including"] = (included_to_including)
  inclusions_db["including_to_included"] = (including_to_included)

  return inclusions_db


# Writes the given output database to disk at the following location:
# <output_dir>/<config_name>/<repo_rev>/
# with the following filename:
# <config_name>_<repo_rev>_inclusions_db.py.
# Warns the user if the above directory already exists.
def WriteInclusionsDbToDisk(inclusions_db, output_dir):
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
def ReadInclusionsDbFromDisk(database_filepath):
  with open(database_filepath, "r") as database_file:
    database = ast.literal_eval(database_file.read())
  return database


# Takes in an inclusions database and returns
# an including_to_included dictionary that has no included files as
# keys.
def FilterOutIncludedFilesAsKeys(inclusions_db):
  included_files = inclusions_db["config"]["included_files"]
  included_files_regexes = [common_utils.RootRegex(f) for f in included_files]

  output_dict = common_utils.DictFilterKeysMatchingRegex(
      inclusions_db["including_to_included"], included_files_regexes)

  return output_dict
