# Library of common functions for analyzing signin code.

import os

# Filters for including files that should *not* be analyzed as external clients
# of signin code.
INCLUDING_FILE_FILTERS = [
    # The Identity Service.
    "^services/identity/.*",
]

# Set of signin clients specified by filename. Each of these clients captures 
# all files that:
# (a) are not captured earlier in the list or in the above list and
# (b) have the client name somewhere in their filepath.
FILENAME_CLIENTS = [
    "account_reconcilor",
    "easy_unlock",
    "account_consistency",
    "dice",
    "child_account_info",
    "gaia_cookie_manager",
    "account_info_fetcher",
    "account_fetcher",
    "account_investigator",
    "about_signin",
    "authentication_service",
    "access_token_fetcher",
    "signin_status_metrics_provider",
    "signin_global_error",
    "signin_promo",
    "force_signin",
    "profile_identity_provider",
    "signin_tracker",
    "proximity_auth",
    "signin_error_notifier",
    "signin_ui_util",
    "refresh_token_annotation_request",
    "signin_capability",
    "oauth2_token_service_observer_bridge",
]

# Set of signin clients specified by directory. Each of these clients captures 
# all files that:
# (a) are not captured earlier in the list or in the above list and
# (b) have the client name as a directory somewhere in their filepath.
DIR_CLIENTS = [
    "ios/web_view/internal/signin",
    "arc/auth",
    "chrome/browser/chromeos/login",
    "chrome/browser/ui/webui/signin",
    "chrome/browser/android/signin",
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
  for client in FILENAME_CLIENTS:
    if client in filename:
      return client

  for client in DIR_CLIENTS:
    if client + "/" in filename:
      return client

  return os.path.dirname(filename)


# Returns a boolean indicating whether |filename| belongs
# to |client|.
def InClient(filename, client):
  return FilenameToSigninClient(filename) == client
