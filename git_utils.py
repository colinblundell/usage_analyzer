# Utilities for working with git.

import os
import subprocess

# Returns the shortrev of HEAD of |repo_root|.
def get_repo_revision(repo_root):
  repo_rev_line = subprocess.Popen("git rev-parse --short HEAD",
                                   shell=True, stdout=subprocess.PIPE,
                                   cwd=repo_root).stdout.read()
  # Strip off the trailing newline.
  return repo_rev_line.strip()

# Returns the shortrev of HEAD of the usage analyzer repo (i.e., this repo).
def get_usage_analyzer_repo_revision():
  return get_repo_revision(
    os.path.dirname(os.path.realpath(__file__)))
