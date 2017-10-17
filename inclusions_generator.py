import subprocess

# Class that analyzes a repository to generate information about the inclusions
# of a given set of files within that repository.
class InclusionsGenerator:
  # Parameters: The configuration for this instance.
  def __init__(self, config):
    self.repo_root = config["repo_root"]
    self.included_files = config["included_files"]

  # Given a filename about which to generate inclusions (relative to the repo
  # root) returns the list of files that include |included_file| in the repo.
  def find_including_files_for_file(self, included_file):
    inclusion_string = '\'include "\'' + included_file
    including_files = subprocess.Popen("git grep -l " + inclusion_string,
                                       shell=True, stdout=subprocess.PIPE,
                                       cwd=self.repo_root).stdout.read()
    return including_files.splitlines()

  # Generates the set of inclusions for the total set of included files
  # Params: None.
  # Returns: a dictionary mapping including filenames to lists of included
  # filenames.
  def find_including_files(self):
    including_files_to_included_files = {}

    for included_file in self.included_files:
      for including_file in self.find_including_files_for_file(included_file):
        if including_file not in including_files_to_included_files:
          including_files_to_included_files[including_file] = []

        including_files_to_included_files[including_file].append(included_file)

    return including_files_to_included_files
