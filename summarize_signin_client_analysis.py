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

signin_clients = common_utils.EvaluateLiteralFromDisk("data/signin/f41c7c32_clients_analysis.py")

summary_keys = [
  "primary account sync access",
  "only primary account sync access",
  "test tasks",
  "test-only",
]

summary_of_clients = {}
weighted_summary_of_clients = {}

def InitializeSummaryIfNecessary(summary):
  for key in summary_keys:
    if key not in summary:
      summary[key] = 0

def UpdateSummary(summary, client_properties, client_value):
  InitializeSummaryIfNecessary(summary)
  if "test tasks" in client_properties:
    summary["test tasks"] += 1
    if len(client_properties.keys()) == 1:
      summary["test-only"] += 1

  if "primary account sync access" in client_properties:
    summary["primary account sync access"] += 1
    # TODO: Also check for only other key being "test tasks".
    if len(client_properties.keys()) == 1:
      summary["only primary account sync access"] += 1

for client_name, client_properties in signin_clients.iteritems():
  UpdateSummary(summary_of_clients, client_properties, 1)
  num_inclusions = client_num_inclusions[client_name]
  UpdateSummary(weighted_summary_of_clients, client_properties, num_inclusions)

print summary_of_clients
print weighted_summary_of_clients
