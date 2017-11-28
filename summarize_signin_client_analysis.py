#!/usr/bin/python
import common_utils

signin_clients = common_utils.EvaluateLiteralFromDisk("data/signin/f41c7c32_clients_analysis.py")

summary_of_clients = {
  "primary account sync access" : 0,
  "only primary account sync access" : 0,
  "test tasks" : 0,
  "test-only" : 0,
}

for client_name, client_properties in signin_clients.iteritems():
  if "test tasks" in client_properties:
    summary_of_clients["test tasks"] += 1
    if len(client_properties.keys()) == 1:
      summary_of_clients["test-only"] += 1

  if "primary account sync access" in client_properties:
    summary_of_clients["primary account sync access"] += 1
    # TODO: Also check for only other key being "test tasks".
    if len(client_properties.keys()) == 1:
      summary_of_clients["only primary account sync access"] += 1

print summary_of_clients
