This repo contains tools to analyze the inclusions of a given set of files
in the codebase over time. There are two fundamental operations:

* Generating a database that has information about the inclusions of a set of
  files.
* Generating analyses that process the information.

We explicitly separate these steps because the first is slow and usually done
only once for a given Chromium revision and set of files to be analyzed, while
the second is fast and may be done many times for a given database.

TO GENERATE A SIGNIN DATABASE

Check out Chromium at the desired revision (most likely at HEAD).
Run the following command:
./generate_inclusions.py /path/to/chromium/src data/database_configs/signin_internals.py data/databases/

TO GENERATE SIGNIN ANALYSES

The easiest thing to do is just regenerate all the analyses, which is still fast
and shouldn't change anything besides adding data for any new databases and/or
analysis configs that you've added.

./scripts/generate_signin_analyses.sh

Once the script is done, the result will be in data/databases/signin_internals/<git_hash>/analyses/

TO ADD THE RESULTS OF AN ANALYSIS TO THE SPREADSHEETS

The spreadsheets live here: 

https://docs.google.com/spreadsheets/d/1KJmaPq5vcDuoeADY0bkQKlNhL73peslwV9QXXmkpEMo/edit#gid=353755218
(request access if you think you need it)

To add the result of a new analysis to the spreadsheets, do the following for
each analysis concerned:
* Run scripts/collate_progress_over_time.sh <analysis-name>
* Any new data should be at the bottom. Copy it.
* Paste it into the relevant sheet on the spreadsheet, click the paste icon and
  click "Split text to columns".
* Pull down on the lowest filled-in cell in the "total" column so that the total
  gets calculated for the new data.
* Observe that the chart gets populated with the new data.

TO MAKE CHANGES TO THE CODEBASE

After making changes, run
./test/run_tests.py

If feasible, add/update any tests if making non-trivial changes.

TODO:
* Find a better place to store data than in the repo. It's unclear where else we
  would store it to allow (a) sharing across users and (b) easy analysis by
  in-repo tooling.
