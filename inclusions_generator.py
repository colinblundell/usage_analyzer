import subprocess

# Given a repo root and a filename about which to generate inclusions,
# returns the list of files that include |included_file| in the repo.
def generateInclusionsForFile(repo_root, included_file):
  inclusion_string = '\'include "\'' + included_file
  inclusions = subprocess.Popen("git grep -l " + inclusion_string, shell=True, stdout=subprocess.PIPE, cwd=repo_root).stdout.read()
  return inclusions.splitlines()

# Given a configuration of files about which to generate inclusions, generates
# the set of inclusions.
# Params: A configuration as specified in XXX.
# Returns: a dictionary mapping including filenames to lists of included
# filenames.
def generateInclusionsForConfig(config):
  repo_root = config["repo_root"]
  included_files = config["included_files"]

  for included_file in included_files:
    inclusions = generateInclusionsForFile(repo_root, included_file)
    print inclusions

  return {}
