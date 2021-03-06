#!/usr/bin/python
import common_utils

from including_to_included_analyzer import IncludingToIncludedAnalyzer
import signin_analysis_lib

database_filename = "/usr/local/google/home/blundell/usage_analyzer_data/signin/f41c7c3273b4/signin_f41c7c3273b4_inclusions_db.py"
including_analyzer = (
    IncludingToIncludedAnalyzer(database_filename,
                                signin_analysis_lib.INCLUDING_FILE_FILTERS))
client_num_inclusions = including_analyzer.GenerateGroupNumInclusionsForFilters(
    signin_analysis_lib.FilenameToSigninClient)

signin_clients = common_utils.EvaluateLiteralFromDisk(
    "data/signin/f41c7c32_clients_analysis.py")

summary_keys = [
    "primary account sync access",
    "primary account sync access only",
    "primary account access token requestor",
    "deferred",
    "only primary account access token requestor",
    "only primary account",
    "primary account read-only",
    "all accounts sync access",
    "all accounts access token requestor",
    "interacts with all accounts",
    "any account read-only",
    "interacts with primary account only",
    "signin/signout observer",
    "token event observer",
    "all accounts signin/signout observer",
    "signin flow",
    "signout flow",
    "signin/signout flow",
    "maybe uses device identity",
    "identity service implementation?",
    "iOS SSO",
    "interacts with java",
    "interacts with platform provider",
    "test tasks",
    "problematic",
    "test-only",
]

display_keys = [
    #"deferred",
    "test tasks",
    "test-only",
    "primary account sync access only",
    "primary account sync access",
    "primary account access token requestor",
    #"primary account read-only",
    "signin/signout observer",
    "token event observer",
    "signin/signout flow",
    "interacts with primary account only",
    "all accounts sync access",
    "all accounts access token requestor",
    "all accounts signin/signout observer",
    #"problematic",
    "interacts with all accounts",
    #"any account read-only",
    "maybe uses device identity",
    "iOS SSO",
    #"interacts with java",
    #"interacts with platform provider",
    "identity service implementation?",
]

summary_of_clients = {}
weighted_summary_of_clients = {}


def InitializeSummaryIfNecessary(summary):
  for key in summary_keys:
    if key not in summary:
      summary[key] = 0


def UpdateSummary(summary, client_properties, client_value):
  InitializeSummaryIfNecessary(summary)

  for key in summary_keys:
    if key in client_properties:
      summary[key] += client_value

  # Calculate composed analyses.
  num_client_properties = len(client_properties.keys())
  has_test_tasks = ("test tasks" in client_properties)
  test_only = has_test_tasks and (num_client_properties == 1)
  device_identity = ("maybe uses device identity" in client_properties)
  all_accounts = ("all accounts sync access" in client_properties or
                  "all accounts access token requestor" in client_properties or
                  "all accounts signin/signout observer" in client_properties)
  ios_sso = ("iOS SSO" in client_properties)
  interacts_with_java = ("interacts with java" in client_properties)
  interacts_with_platform_provider = ios_sso or interacts_with_java
  signin_signout_flow = ("signin flow" in client_properties or
                         "signout flow" in client_properties)
  identity_service_impl = (
      "identity service implementation?" in client_properties)
  primary_account_only = not (device_identity or all_accounts or ios_sso or
                              identity_service_impl)
  primary_account_read_only = primary_account_only and not signin_signout_flow
  is_problematic = all_accounts or ios_sso or device_identity or identity_service_impl

  if signin_signout_flow:
    summary["signin/signout flow"] += client_value

  if test_only:
    summary["test-only"] += client_value

  if all_accounts:
    summary["interacts with all accounts"] += client_value

  if interacts_with_platform_provider:
    summary["interacts with platform provider"] += client_value

  if num_client_properties == 1 or (num_client_properties == 2 and
                                    has_test_tasks):
    if "primary account sync access" in client_properties:
      summary["primary account sync access only"] += client_value
    if "primary account access token requestor" in client_properties:
      summary["only primary account access token requestor"] += client_value

  if primary_account_only:
    summary["interacts with primary account only"] += client_value
  if primary_account_read_only:
    summary["primary account read-only"] += client_value

  if is_problematic:
    summary["problematic"] += client_value

  #is_problematic = "signin flow" in client_properties or "signout flow" in client_properties or "maybe uses device identity" in client_properties or "iOS SSO" in client_properties or "update credentials" in client_properties or "interacts with java" in client_properties
  #if not is_problematic:
  #  summary["any account read-only"] += client_value

  #primary_account_only = not (is_problematic or "all accounts sync access" in client_properties or "all accounts access token requestor" in client_properties or "all accounts signin/signout observer" in client_properties)
  #if primary_account_only:
  #  summary["primary account read-only"] += client_value


for client_name, client_properties in signin_clients.iteritems():
  UpdateSummary(summary_of_clients, client_properties, 1)
  num_inclusions = client_num_inclusions[client_name]
  UpdateSummary(weighted_summary_of_clients, client_properties, num_inclusions)

# Display the results in CSV format suitable for outputting into a spreadsheet.
total_num_clients = len(signin_clients.keys())
total_num_inclusions = client_num_inclusions["total"]
print "Characteristic, %% of %d clients, %% of clients weighted by size" % (
    total_num_clients)
for key in display_keys:
  num_clients = summary_of_clients[key]
  num_inclusions = weighted_summary_of_clients[key]
  percent_of_clients = float(num_clients) / float(total_num_clients) * 100.0
  percent_of_inclusions = float(num_inclusions) / float(
      total_num_inclusions) * 100.0
  print "%s,%.0f,%.0f" % (key, percent_of_clients, percent_of_inclusions)
