# Utilities for working with git.

import subprocess

# Returns the shortrev of HEAD of |repo_root|.
def get_repo_revision(repo_root):
  return subprocess.Popen("git rev-parse --short HEAD",
                          shell=True, stdout=subprocess.PIPE,
                          cwd=repo_root).stdout.read()
