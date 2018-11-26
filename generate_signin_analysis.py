#!/usr/bin/python

import copy
import os
import shutil
import sys

from included_to_including_analyzer import IncludedToIncludingAnalyzer
from including_to_included_analyzer import IncludingToIncludedAnalyzer
from including_to_included_analyzer import ComputeGroupNumInclusionsDeltaBetween
import common_utils
import inclusions_database
import signin_analysis_lib


def GenerateAnalyses(database_filename, included_files_to_limit_to_filename):
  analyses_name = "total"
  included_files_to_limit_to = None
  if included_files_to_limit_to_filename:
    included_files_to_limit_to_dict = common_utils.EvaluateLiteralFromDisk(
        included_files_to_limit_to_filename)
    analyses_name = included_files_to_limit_to_dict["name"]
    included_files_to_limit_to = included_files_to_limit_to_dict[
        "included_files_to_limit_to"]

  output_dir = os.path.join(
      os.path.dirname(database_filename), "analyses", analyses_name)
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  including_analyzer = (
      IncludingToIncludedAnalyzer(database_filename,
                                  signin_analysis_lib.INCLUDING_FILE_FILTERS))

  # Generate progress-over-time input.

  features_num_inclusions = including_analyzer.GenerateGroupNumInclusions(
      signin_analysis_lib.FilenameToSigninClient)
  for name, analysis in features_num_inclusions:
    if name == "# inclusions":
      total_inclusions = analysis["total"]
    elif name == "from prod":
      prod_inclusions = analysis["total"]
    elif name == "from prod non-factory":
      prod_non_factory_inclusions = analysis["total"]
    else:
      assert 0

  date = including_analyzer.inclusions_db["repo_commit_date"]
  test_inclusions = total_inclusions - prod_inclusions
  prod_factory_inclusions = prod_inclusions - prod_non_factory_inclusions
  progress_over_time_input = "%s,%d,%d,%d\n" % (date, test_inclusions,
                                                prod_factory_inclusions,
                                                prod_non_factory_inclusions)
  progress_over_time_input_filename = os.path.join(
      output_dir, "progress_over_time_input.txt")
  with open(progress_over_time_input_filename, "w") as f:
    f.write(progress_over_time_input)

  # Generate delta from last state.

  previous_database_filename = inclusions_database.FindMostRecentDbBefore(
      database_filename)
  previous_database_commit_date = inclusions_database.GetRepoCommitDateFromInclusionsDbFilename(
      previous_database_filename)

  delta_since_last_state = ComputeGroupNumInclusionsDeltaBetween(
      previous_database_filename, database_filename, lambda filename: filename)
  changed_files = delta_since_last_state[0][1].keys()
  key_order = copy.deepcopy(changed_files)
  key_order.sort()

  # Generate the status of each of the dependencies that has changed (i.e., is
  # it a new dependency, an ongoing dependency, or a completed dependency), and
  # append it to the analysis.
  changed_files_status = {}
  prev_db = inclusions_database.ReadInclusionsDbFromDisk(
      previous_database_filename)
  for filename in key_order:
    if filename not in prev_db["including_to_included"]:
      status = "New"
    elif filename not in including_analyzer.including_file_dict:
      status = "Completed"
    else:
      status = "Ongoing"
    changed_files_status[filename] = status
  delta_since_last_state.append(["Dependency status", changed_files_status])

  delta_since_last_state_csv = including_analyzer.GenerateCsvFromGroupAnalysis(
      delta_since_last_state, "feature", key_order=key_order)
  delta_since_last_state_filename = os.path.join(
      output_dir, "delta_since_%s.txt" % previous_database_commit_date)
  with open(delta_since_last_state_filename, "w") as f:
    f.write(delta_since_last_state_csv)

  # Generate detailed breakdowns of current state.
  feature_list = including_analyzer.GroupsOrderedByNumInclusions(
      signin_analysis_lib.FilenameToSigninClient)

  features_num_inclusions_csv = including_analyzer.GenerateGroupAnalysisAsCsv(
      "num_inclusions", signin_analysis_lib.FilenameToSigninClient, "feature")
  features_num_inclusions_filename = os.path.join(
      output_dir, "features_num_inclusions.txt")
  with open(features_num_inclusions_filename, "w") as f:
    f.write(features_num_inclusions_csv)

  features_num_including_files_csv = including_analyzer.GenerateGroupAnalysisAsCsv(
      "group_size",
      signin_analysis_lib.FilenameToSigninClient,
      "feature",
      key_order=feature_list)
  features_num_including_files_filename = os.path.join(
      output_dir, "features_num_including_files.txt")
  with open(features_num_including_files_filename, "w") as f:
    f.write(features_num_including_files_csv)

  features_analyses_dir = os.path.join(output_dir, "features")
  if os.path.exists(features_analyses_dir):
    shutil.rmtree(features_analyses_dir)
  os.mkdir(features_analyses_dir)
  for feature in feature_list:
    feature_analysis = including_analyzer.GenerateNumInclusionsForFilterFunction(
        lambda f: signin_analysis_lib.InClient(f, feature))
    # Sort files in alphabetical order for the individual feature analysis to
    # group directories together.
    including_files_order = copy.deepcopy(feature_analysis.keys())
    including_files_order.sort()
    feature_analysis_csv = common_utils.DictToCsv(
        feature_analysis, ["file", "# inclusions"], including_files_order)
    feature_analysis_filename = os.path.join(features_analyses_dir,
                                             feature.replace("/", "_") + ".txt")
    with open(feature_analysis_filename, "w") as f:
      f.write(feature_analysis_csv)

  included_analyzer = (
      IncludedToIncludingAnalyzer(database_filename,
                                  signin_analysis_lib.INCLUDING_FILE_FILTERS))
  included_files_analysis = included_analyzer.GenerateAnalysis()
  included_files_order = common_utils.DictKeysSortedByValue(
      included_files_analysis)
  included_files_analysis_csv = common_utils.DictToCsv(
      included_files_analysis, ["file", "# inclusions"], included_files_order)
  included_files_analysis_filename = os.path.join(
      output_dir, "included_files_analysis.txt")
  with open(included_files_analysis_filename, "w") as f:
    f.write(included_files_analysis_csv)


if __name__ == '__main__':
  database_path = sys.argv[1]
  included_files_to_limit_to_path = None
  if len(sys.argv) == 3:
    included_files_to_limit_to_path = sys.argv[2]

  GenerateAnalyses(database_path, included_files_to_limit_to_path)
