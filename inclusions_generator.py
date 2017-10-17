import subprocess

# Given a repo root and a filename about which to generate inclusions,
# returns the list of files that include |included_file| in the repo.
def find_including_files_for_file(repo_root, included_file):
  inclusion_string = '\'include "\'' + included_file
  including_files = subprocess.Popen("git grep -l " + inclusion_string, shell=True, stdout=subprocess.PIPE, cwd=repo_root).stdout.read()
  return including_files.splitlines()

# Given a configuration of files about which to generate inclusions, generates
# the set of inclusions.
# Params: A configuration as specified in XXX.
# Returns: a dictionary mapping including filenames to lists of included
# filenames.
def find_including_files(config):
  repo_root = config["repo_root"]
  included_files = config["included_files"]

  including_files_to_included_files = {}
  for included_file in included_files:
    for including_file in findIncludingFilesForFile(repo_root, included_file):
      if including_file not in including_files_to_included_files:
        including_files_to_included_files[including_file] = []
      including_files_to_included_files[including_file].append(included_file)

  return including_files_to_included_files
