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
    "only primary account sync access",
    "primary account access token requestor",
    "only primary account access token requestor",
    "only primary account",
    "all accounts sync access",
    "all accounts access token requestor",
    "standard",
    "signin/signout observer",
    "token event observer",
    "signin flow",
    "signout flow",
    "signin/signout flow",
    "maybe uses device identity",
    "iOS-specific",
    "test tasks",
    "test-only",
]

display_keys = [
    "standard",
    "primary account sync access",
    "primary account access token requestor",
    "all accounts sync access",
    "all accounts access token requestor",
    "signin/signout observer",
    "token event observer",
    "signin/signout flow",
    "maybe uses device identity",
    "test tasks",
]

summary_of_clients = {}
weighted_summary_of_clients = {}


def InitializeSummaryIfNecessary(summary):
  for key in summary_keys:
    if key not in summary:
      summary[key] = 0


def UpdateSummary(summary, client_properties, client_value):
  num_client_properties = len(client_properties.keys())
  has_test_tasks = ("test_tasks" in client_properties)
  InitializeSummaryIfNecessary(summary)

  for key in summary_keys:
    if key in client_properties:
      summary[key] += client_value

  if "signin flow" in client_properties or "signout flow" in client_properties:
    summary["signin/signout flow"] += client_value

  if num_client_properties == 1 or (num_client_properties == 2 and
                                    has_test_tasks):
    if "test tasks" in client_properties:
      summary["test-only"] += client_value
    if "primary account sync access" in client_properties:
      summary["only primary account sync access"] += client_value
    if "primary account access token requestor" in client_properties:
      summary["only primary account access token requestor"] += client_value

  is_problematic = "signin flow" in client_properties or "signout flow" in client_properties or "maybe uses device identity" in client_properties or "iOS-specific" in client_properties or "update credentials" in client_properties
  #is_problematic = "signin flow" in client_properties or "signout flow" in client_properties
  if not is_problematic:
    summary["standard"] += client_value

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
