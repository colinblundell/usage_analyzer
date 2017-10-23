import inclusions_config
import subprocess
import sys


# Class that analyzes a repository to generate information about the inclusions
# of a given set of files within that repository.
class InclusionsGenerator:
  # Parameters: The configuration for this instance, as defined in config.py.
  def __init__(self, config):
    inclusions_config.validate_config(config)
    self.config = config

  # Given a filename about which to generate inclusions (relative to the repo
  # root), returns the list of files that include |included_file| in the repo.
  def find_including_files_for_file(self, included_file):
    inclusion_string = '\'include "\'' + included_file
    including_files = subprocess.Popen(
        "git grep -l " + inclusion_string,
        shell=True,
        stdout=subprocess.PIPE,
        cwd=self.config["evaluated_repo_root"]).stdout.read()
    return including_files.splitlines()

  # Generates the mapping of including files to included files for the total set
  # of included files.
  # Params: None.
  # Returns: a dictionary mapping including filenames to lists of included
  # filenames.
  def map_including_to_included(self):
    including_to_included = {}

    for included_file in self.config["included_files"]:
      for including_file in self.find_including_files_for_file(included_file):
        if including_file not in including_to_included:
          including_to_included[including_file] = []

        including_to_included[including_file].append(included_file)

    return including_to_included

  # Generates the mapping of included files to including files for the total set
  # of included files.
  # Params: None.
  # Returns: a dictionary mapping included filenames to lists of including
  # filenames.
  def map_included_files_to_including_files(self):
    included_files_to_including_files = {}

    including_to_included = (
        self.map_including_to_included())
    for including_file, included_files in (
        including_to_included.items()):

      for included_file in included_files:
        if included_file not in included_files_to_including_files:
          included_files_to_including_files[included_file] = []

        included_files_to_including_files[included_file].append(including_file)

    return included_files_to_including_files
