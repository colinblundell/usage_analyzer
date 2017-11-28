# Definition of inclusions database dictionaries and facilities to
# operate on them (move them to/from disk, generate databases, ...).

import datetime
import glob
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
    # The commit date of the repo that was analyzed (i.e., the repo
    # specified by the configuration's |evaluated_repo_root| field).
    # In YYYY/MM/DD form.
    "repo_commit_date": "short-commit-date",
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

  repo_commit_date = git_utils.GetRepoCommitDate(config["evaluated_repo_root"])
  inclusions_db["repo_commit_date"] = repo_commit_date

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
  return common_utils.EvaluateLiteralFromDisk(database_filepath)


def IncludedFilesRegexes(inclusions_db):
  included_files = inclusions_db["config"]["included_files"]
  root_regexes = [common_utils.RootRegex(f) for f in included_files]
  test_regexes = [common_utils.UnittestRegex(f) for f in included_files]
  included_files_regexes = root_regexes + test_regexes
  return included_files_regexes


# Takes in an inclusions database and returns
# an including_to_included dictionary that has no included files as
# keys.
def FilterOutIncludedFilesAsKeys(inclusions_db):
  output_dict = common_utils.DictFilterKeysMatchingRegex(
      inclusions_db["including_to_included"],
      IncludedFilesRegexes(inclusions_db))

  return output_dict


# Takes in an inclusions database and returns
# an included_to_including dictionary that has no included files as
# values.
def FilterOutIncludedFilesAsValues(inclusions_db):
  output_dict = common_utils.DictFilterValuesMatchingRegex(
      inclusions_db["included_to_including"],
      IncludedFilesRegexes(inclusions_db))

  return output_dict


# Takes in a filepath to an inclusions database and returns the repo commit date
# for the databes.
def GetRepoCommitDateFromInclusionsDbFilename(database_filepath):
  db = ReadInclusionsDbFromDisk(database_filepath)
  return db["repo_commit_date"]


# Given |database_filepath|, returns the filepath of the database in the same
# analysis that was generated most recently prior to the generation of the
# database in |database_filepath|. "The same analysis" here refers to all
# database residing in peer directories of the parent directory of
# |database_filepath|.
def FindMostRecentDbBefore(database_filepath):
  target_repo_commit_date = GetRepoCommitDateFromInclusionsDbFilename(
      database_filepath)
  most_recent_db_path = None
  most_recent_db_commit_date = None
  base_dir = os.path.dirname(os.path.dirname(database_filepath))
  for peer_db_filepath in glob.glob("%s/*/*inclusions_db.py" % base_dir):
    if peer_db_filepath == database_filepath:
      continue
    peer_repo_commit_date = GetRepoCommitDateFromInclusionsDbFilename(
        peer_db_filepath)
    if not most_recent_db_commit_date or (
        (peer_repo_commit_date < target_repo_commit_date) and
        (peer_repo_commit_date > most_recent_db_commit_date)):
      most_recent_db_commit_date = peer_repo_commit_date
      most_recent_db_path = peer_db_filepath
  return most_recent_db_path
