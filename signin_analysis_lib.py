# Library of common functions for analyzing signin code.

import os

# Filters for including files that should *not* be analyzed as external clients
# of signin code.
INCLUDING_FILE_FILTERS = [
    # The Identity Service.
    "^services/identity/.*",
]

# Set of signin clients. Each of these clients captures all files that:
# (a) are not captured earlier in the list and
# (b) have the client name somewhere in their filepath.
CLIENTS = [
    "ios/web_view/internal/signin",
    "arc/auth",
    "chrome/browser/chromeos/login",
    "sync",
    "signin",
    "history",
    "autofill",
    "password",
    "policy",
    "supervised_user",
    "gcm",
    # NOTE: This must be below sync and gcm to avoid catching their driver dirs.
    "drive",
    "invalidation",
    "ntp_snippets",
    "suggestions",
    "profiles",
    "google_apis",
    "settings",
    "payments",
    "cryptauth",
    "first_run",
    "bookmarks",
    "chrome/browser/extensions/api/identity",
    "webui",
    "ios/chrome/browser/ui",
    "chrome/browser/ui",
    "extensions",
]


# Maps a filename into the signin client that it belongs to.
def FilenameToSigninClient(filename):
  for client in CLIENTS:
    if client in filename:
      return client

  return os.path.dirname(filename)


# Returns a boolean indicating whether |filename| belongs
# to |client|.
def InClient(filename, client):
  return FilenameToSigninClient(filename) == client
