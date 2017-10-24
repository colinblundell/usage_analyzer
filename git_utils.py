# Utilities for working with git.

import os
import subprocess


# Returns the shortrev of HEAD of |repo_root|.
def GetRepoRevision(repo_root):
  repo_rev_line = subprocess.Popen(
      "git rev-parse --short HEAD",
      shell=True,
      stdout=subprocess.PIPE,
      cwd=repo_root).stdout.read()
  # Strip off the trailing newline.
  return repo_rev_line.strip()


# Returns the shortrev of HEAD of the usage analyzer repo (i.e., this repo).
def GetUsageAnalyzerRepoRevision():
  return GetRepoRevision(os.path.dirname(os.path.realpath(__file__)))
