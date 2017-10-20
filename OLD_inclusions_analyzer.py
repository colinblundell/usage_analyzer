#!/usr/bin/python

import os
import subprocess

from operator import itemgetter

INPUT_FILES = [
"components/signin/core/browser/account_fetcher_service",
"components/signin/core/browser/account_tracker_service",
"components/signin/core/browser/profile_oauth2_token_service",
"components/signin/core/browser/signin_manager_base",
"components/signin/core/browser/signin_manager",
"components/sync/driver/signin_manager_wrapper",
"google_apis/gaia/oauth2_token_service",
]

EXCLUDED_DIRECTORIES = [
"services/identity",
]

# Listed in priority order, i.e., earlier entries are prioritized
# for matching over later entries.
CATCHALLS = [
#"ios/chrome/browser/ui",
#"chrome/browser/ui",
#"ios",
]

CLIENTS = [
"ios/web_view/internal/signin",
"arc/auth",
"login",
"sync",
"signin",
"history",
"autofill",
"password",
"policy",
"supervised_user",
"gcm",
# NOTE: This should be below sync and gcm to avoid catching their driver dirs.
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
"api/identity",
# TODO: Should I restore these?
"chrome/browser/extensions",
#"extensions",
"webui",
]

CLIENTS += CATCHALLS

def collect_inclusions_of_file(input_file, prod_inclusions_by_directory,
                               test_inclusions_by_directory,
                               prod_including_files_by_directory):
  inclusion_string = '\'include "\'' + input_file
  inclusions = subprocess.Popen("git grep -l " + inclusion_string, shell=True, stdout=subprocess.PIPE,
                                cwd=os.getenv("HOME") + "/chromium/src").stdout.read()
  for filename in inclusions.splitlines():
    if os.path.splitext(filename)[0] in INPUT_FILES:
      continue
    parent_dir = os.path.dirname(filename)
    if parent_dir in EXCLUDED_DIRECTORIES:
      continue
    dictionary = prod_inclusions_by_directory
    is_prod = True
    if "test" in filename or "fake" in filename:
      dictionary = test_inclusions_by_directory
      is_prod = False
    if parent_dir not in dictionary:
      dictionary[parent_dir] = 0
    dictionary[parent_dir] += 1
    if is_prod:
      if parent_dir not in prod_including_files_by_directory:
        prod_including_files_by_directory[parent_dir] = set()
      prod_including_files_by_directory[parent_dir].add(filename)

def analyze_inclusions():
  prod_inclusions_by_directory = {}
  test_inclusions_by_directory = {}
  prod_including_files_by_directory = {}

  for input_file in INPUT_FILES:
    print "Analyzing", input_file

    collect_inclusions_of_file(input_file, prod_inclusions_by_directory,
                               test_inclusions_by_directory,
                               prod_including_files_by_directory)

  print
  print "Prod inclusions:"
  clients_to_including_files = {}
  clients_to_inclusions = {}
  clients_to_dirs = {}
  catchalls_to_inclusions = {}
  catchalls_to_dirs = {}
  total_inclusions = 0
  total_catchall_inclusions = 0
  for directory, num_inclusions in sorted(prod_inclusions_by_directory.items(), key=itemgetter(1), 
                     reverse=True):
    client_to_use = directory
    for client in CLIENTS:
      if client in directory:
        client_to_use = client
        break
    to_inclusions = clients_to_inclusions
    to_dirs = clients_to_dirs
    total_inclusions += num_inclusions
    if client_to_use in CATCHALLS:
      to_inclusions = catchalls_to_inclusions
      to_dirs = catchalls_to_dirs
      total_catchall_inclusions += num_inclusions
    if client_to_use not in to_inclusions:
      to_inclusions[client_to_use] = 0
      to_dirs[client_to_use] = []
      clients_to_including_files[client_to_use] = set()
    to_inclusions[client_to_use] += num_inclusions
    clients_to_including_files[client_to_use] = clients_to_including_files[client_to_use].union(prod_including_files_by_directory[directory])
    if client_to_use != directory:
      to_dirs[client_to_use].append(directory + ": " + str(num_inclusions))

  print "Total inclusions:", total_inclusions

  print "Total feature clients: ", len(clients_to_inclusions.keys())
  print "Total feature client inclusions:", total_inclusions - total_catchall_inclusions
  print
  clients_in_category = 0
  inclusions_in_category = 0
  category = "giant"
  summary = ""
  for client, num_inclusions in sorted(clients_to_inclusions.items(), key=itemgetter(1), 
                     reverse=True):
    if category == "giant" and num_inclusions < 50:
      print "Summary of giant features:", clients_in_category, "clients with", inclusions_in_category, "inclusions"
      clients_in_category = 0
      inclusions_in_category = 0
      category = "large"
      print
    if category == "large" and num_inclusions < 10:
      print "Summary of large features:", clients_in_category, "clients with", inclusions_in_category, "inclusions"
      clients_in_category = 0
      inclusions_in_category = 0
      category = "medium"
      print
    if category == "medium" and num_inclusions < 4:
      print "Summary of medium features:", clients_in_category, "clients with", inclusions_in_category, "inclusions"
      clients_in_category = 0
      inclusions_in_category = 0
      category = "small"
      print
    clients_in_category += 1
    inclusions_in_category += num_inclusions
    print client + ":", num_inclusions, "inclusions"
    for including_dir in clients_to_dirs[client]:
      print "  " + including_dir
    if category == "giant":
      print "Including files: "
      including_files = list(clients_to_including_files[client])
      including_files.sort()
      for f in including_files:
        if "factory" not in f:
          print f

  print "Summary of small features:", clients_in_category, "clients with", inclusions_in_category, "inclusions"
  
#  print "Total catchalls: ", len(catchalls_to_inclusions.keys())
#  print "Total catchall inclusions:", total_catchall_inclusions
#  print
#  for catchall, num_inclusions in sorted(catchalls_to_inclusions.items(), key=itemgetter(1), 
#                     reverse=True):
#    print catchall + ":", num_inclusions, "inclusions"
#    for including_dir in catchalls_to_dirs[catchall]:
#      print "  " + including_dir
#    print
