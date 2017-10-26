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
    "password_manager",
    "policy",
    "supervised_user",
    "gcm",
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
    "browsing_data",
    "chrome/browser/extensions/api/identity",
    "webui",
    "autocomplete",
    "feedback",
    "browser_state",
    "cloud_print",
    "metrics",
    "download",
    "safe_browsing",
    "drive_backend",
    "gcm_driver",
    "desktop_ios_promotion",
    "search",
    "toolbar",
    "devtools",
    "startup",
    "app_list",
    "ios/chrome/browser/ui/authentication",
    "ios/chrome/browser/ui/signin_interaction",
    "ios/chrome/browser/ui",
    "chrome/browser/ui",
    "extensions",
    "chrome/browser/android",
    "chrome/browser/chromeos",
]


# Maps a filename into the signin client that it belongs to.
def FilenameToSigninClient(filename):
  for client in CLIENTS:
    if client + "/" in filename:
      return client

  return os.path.dirname(filename)


# Returns a boolean indicating whether |filename| belongs
# to |client|.
def InClient(filename, client):
  return FilenameToSigninClient(filename) == client
